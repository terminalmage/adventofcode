#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/25
'''
import itertools
from typing import Literal

# Local imports
from aoc import AOC
from day12 import Computer, Instruction, Program


class SignalGenerator(Computer):
    '''
    Modified Computer which implements "out" command
    '''
    def run(self, program: Program, **init: int) -> bool:
        '''
        Run the program (which should run indefinitely), while keeping track of
        the signals that are emitted by it. The puzzle is looking for an
        endless repeating cycle of 0 and 1 (e.g 0, 1, 0, 1 ....). We can't test
        for infinity (obviously), so treat 24 consecutive alternating signals
        as a True result. Any deviation from that is a False result.
        '''
        # Apply any initial values passed in
        self.init(**init)

        # Index of where we are in the program's instruction set
        index: int = 0

        Signal = Literal[0, 1]
        signals: list[Signal] = []

        while index < len(program):
            instruction: Instruction = program[index]

            match instruction.split():
                case ['out', register]:
                    signal: Signal = self.resolve(register)
                    if signal not in (0, 1):
                        return False
                    signals.append(signal)

                    if any(
                        x != y for x, y in zip(
                            signals,
                            itertools.cycle((signals[0], 1 - signals[0]))
                        )
                    ):
                        return False

                    if len(signals) == 24:
                        # Assume 24 consecutive repeating digits is a success
                        # (this is probably overkill)
                        return True

                case _:
                    # The command wasn't a custom command. fall back to the
                    # parent class' instruction-handling logic to both process
                    # the instruction and get the index of the next instruction
                    # to run, and then skip to the next loop iteration.
                    index = self.exec(index, instruction)
                    continue

            # Custom argument handling was used, point the index at the
            # next instruction in the program.
            index += 1


class AOC2016Day25(AOC):
    '''
    Day 25 of Advent of Code 2016
    '''
    def post_init(self) -> None:
        '''
        Initialize the SignalGenerator and load the program from the puzzle input
        '''
        self.generator: SignalGenerator = SignalGenerator()
        # Detect and optimize loops. Note that this is done here rather than in
        # the Generator class' run() method because we will need to run that
        # method many times, and we only want to optimize the program once.
        self.program: Program = self.generator.optimize(self.input.splitlines())

    def part1(self) -> int:
        '''
        Run the program with incrementing values for register a until it begins
        to emit an infinitely-repeating alternating sequence of 0 and 1
        signals.
        '''
        for a in itertools.count(1):
            if self.generator.run(self.program, a=a):
                return a


if __name__ == '__main__':
    # Run against actual data
    aoc = AOC2016Day25(example=False)
    aoc.run()
