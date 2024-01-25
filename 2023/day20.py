#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/20
'''
from __future__ import annotations
import functools
import math
import textwrap
from collections import deque
from dataclasses import dataclass
from typing import Literal

# Local imports
from aoc import AOC

# Typing shortcuts
HighPulse = On = True
LowPulse = Off = False
Pulse = FlipFlopState = Literal[HighPulse, LowPulse]
PulseOutput = tuple['Module', Pulse] | None


class Module:
    '''
    Base class for modules
    '''
    def __init__(self, name: str) -> None:
        '''
        Initialize inputs and outputs
        '''
        self.name: str = name
        self.outputs: list[Module] = []

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'{self.__class__.__name__}(name={self.name!r})'

    def add_output(self, module: Module) -> None:
        '''
        Function to add a module to this module's outputs
        '''
        self.outputs.append(module)

    def pulse(
        self,
        sender: Module,   # pylint: disable=unused-argument
        pulse: Pulse,     # pylint: disable=unused-argument
    ) -> PulseOutput:
        '''
        Read incoming pulse and output the appropriate pulse
        '''
        raise NotImplementedError

    def reset(self) -> None:
        '''
        Reset module to initial state (no-op unless implemented in subclass)
        '''


class Broadcaster(Module):
    '''
    Module which broadcasts whichever pulse is sent to it
    '''
    def __init__(self) -> None:
        '''
        Initialize module
        '''
        super().__init__(name='broadcaster')

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return 'Broadcaster()'

    def pulse(  # pylint: disable=arguments-differ
        self,
        pulse: Pulse,
    ) -> PulseOutput:
        '''
        Read incoming pulse and output the appropriate pulse
        '''
        return self, pulse


class FlipFlop(Module):
    '''
    Acts like a switch. When a low pulse is received, its value is flipped
    and the corresponding pulse is sent. When a high pulse is received, nothing
    is done.
    '''
    def __init__(self, name: str) -> None:
        '''
        Initialize module
        '''
        super().__init__(name)
        # Initial state is off
        self.value: FlipFlopState = Off

    def pulse(
        self,
        sender: Module,  # pylint: disable=unused-argument
        pulse: Pulse,
    ) -> PulseOutput:
        '''
        Read incoming pulse and output the appropriate pulse
        '''
        if pulse is LowPulse:
            # Flip the value and output that value as a Pulse
            # True = on = HighPulse
            # False = off = LowPulse
            self.value: FlipFlopState = not self.value
            return self, self.value

        # No action if HighPulse received
        return None

    def reset(self) -> None:
        '''
        Reset module to initial state
        '''
        self.value: bool = False


class Conjunction(Module):
    '''
    Outputs a low pulse if all input registers are set to True, otherwise
    outputs a high pulse.
    '''
    def __init__(self, name: str) -> None:
        '''
        Initialize module
        '''
        super().__init__(name)
        self.registers: dict[Module, Pulse] = {}

    def add_input(self, module: Module) -> None:
        '''
        Initialize the last received pulse from the newly-added input
        '''
        self.registers[module]: Pulse = LowPulse

    def pulse(
        self,
        sender: Module,
        pulse: Pulse,
    ) -> PulseOutput:
        '''
        Read incoming pulse and output the appropriate pulse
        '''
        # Update input register
        self.registers[sender]: Pulse = pulse
        # Output a low pulse if all input registers are set to True
        if all(p is HighPulse for p in self.registers.values()):
            return self, LowPulse
        # Output a high pulse
        return self, HighPulse

    def reset(self) -> None:
        '''
        Reset module to initial state
        '''
        self.registers = self.registers.fromkeys(self.registers, 0)


class Output(Module):
    '''
    Dummy module that does not have any outputs and does not respond to pulses
    '''
    def pulse(
        self,
        sender: Module,  # pylint: disable=unused-argument
        pulse: Pulse,    # pylint: disable=unused-argument
    ) -> PulseOutput:
        '''
        Read incoming pulse and output the appropriate pulse
        '''
        return None


@dataclass
class PulseCount:
    '''
    Aggregates low and high counts
    '''
    low: int = 0
    high: int = 0

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'PulseCount(low={self.low}, high={self.high})'

    def __add__(self, other: 'PulseCount'):
        '''
        Implement addition, returning a new PulseCount
        '''
        return PulseCount(
            low=self.low + other.low,
            high=self.high + other.high,
        )

    def __iadd__(self, other: 'PulseCount'):
        '''
        Implement addition in-place
        '''
        self.low += other.low
        self.high += other.high


class Machine:
    '''
    State machine which maintains a queue to ensure pulses are processed in the
    correct order
    '''
    def __init__(self, data: str):
        '''
        Load the machine configuration from the input file
        '''
        self.modules: dict[str, Module] = {}

        # Do a first pass on the input file to instantiate all the modules
        output_map: dict[Module, str] = {}
        for line in data.splitlines():
            label: str
            outputs: str
            label, outputs = line.split(' -> ')
            if label.startswith('%'):
                label = label[1:]
                module = FlipFlop(label)
            elif label.startswith('&'):
                label = label[1:]
                module = Conjunction(label)
            elif label == 'broadcaster':
                module = Broadcaster()
            else:
                raise ValueError(f'Invalid module {label!r}')

            self.modules[label]: Module = module
            output_map[module]: list[str] = outputs.split(', ')

        self.rx_parent: str | None = None

        # Now that all the modules have been instantiated, assign all outputs
        module: Module
        outputs: list[str]
        for module, outputs in output_map.items():
            output_label: str
            for output_label in outputs:
                if output_label not in self.modules:
                    # Output is a dummy output module
                    output: Output
                    output = self.modules[output_label] = Output(output_label)
                    if output_label == 'rx':
                        self.rx_parent = module.name
                else:
                    # Locate output module
                    output: Module = self.modules[output_label]
                # Append to the module's outputs
                module.outputs.append(output)
                # If output is a Conjunction, add the module to the
                # Conjunction's inputs
                if isinstance(output, Conjunction):
                    output.add_input(module)

        self.presses = self.rx_parent_inputs = self.rx_lcm = None
        self.reset()

    def reset(self) -> None:
        '''
        Reset all modules, counters, etc. to initial state
        '''
        module: Module
        for module in self.modules.values():
            module.reset()

        self.presses: int = 0
        if self.rx_parent is not None:
            self.rx_parent_inputs: dict[Module, int] = {
                module: 0 for module in self.modules[self.rx_parent].registers
            }
        else:
            self.rx_parent_inputs = {}
        self.rx_lcm: int = 0

    def press_button(self) -> PulseCount:
        '''
        Send a signal to the Broadcaster
        '''
        # Increment button press count
        self.presses += 1

        # Initialize pulse counter for this button press. Don't forget to count
        # the low pulse sent by the button itself.
        counter: PulseCount = PulseCount(low=1)

        # Initialize queue
        pulses: deque[tuple[Module, Pulse]] = deque(
            [self.modules['broadcaster'].pulse(LowPulse)]
        )

        while pulses:
            try:
                # Read from queue
                sender: Module
                pulse: Pulse
                sender, pulse = pulses.popleft()
            except TypeError:
                # No pulse was output
                continue

            # This module will send one pulse to each of its outputs. Increment
            # the appropriate pulse counter by this module's number of outputs.
            if pulse is HighPulse:
                # Update the number of high pulses
                counter.high += len(sender.outputs)

                # Track the button press when each of the inputs to the parent
                # module of the "rx" output module first get a high pulse.
                if (
                    sender in self.rx_parent_inputs
                    and not self.rx_parent_inputs[sender]
                ):
                    self.rx_parent_inputs[sender]: int = self.presses
                    # Since we've just changed the value, re-calculate the LCM
                    self.rx_lcm: int = math.lcm(*self.rx_parent_inputs.values())

            else:
                # Update the number of low pulses
                counter.low += len(sender.outputs)

            # Enqueue pulses for all outputs
            for output in sender.outputs:
                pulses.append(output.pulse(sender, pulse))

        return counter


class AOC2023Day20(AOC):
    '''
    Day 20 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        broadcaster -> a, b, c
        %a -> b
        %b -> c
        %c -> inv
        &inv -> a
        '''
    )

    validate_part1: int = 32000000

    def part1(self) -> int:
        '''
        Return the sum of the ratings (i.e. the sum of all 4 categories) for
        each accpeted part.
        '''
        machine = Machine(self.input)
        count = functools.reduce(
            lambda x, y: x + y,
            (machine.press_button() for _ in range(1000))
        )
        return count.low * count.high

    def part2(self) -> int:
        '''
        Return the fewest number of button presses required to send a pulse to
        the rx output.
        '''
        machine = Machine(self.input)

        while machine.rx_lcm == 0:
            machine.press_button()

        return machine.rx_lcm


if __name__ == '__main__':
    aoc = AOC2023Day20()
    aoc.run()
