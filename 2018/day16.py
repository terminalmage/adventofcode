#!/usr/bin/env python
"""
https://adventofcode.com/2018/day/16
"""
import inspect
import re
import textwrap
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

# Local imports
from aoc import AOC


# Type hints
OpcodeNumber = int
OpcodeName = str
Input = int
Output = int
Instruction = tuple[OpcodeNumber, Input, Input, Output]
Program = tuple[Instruction, ...]
Register = int
Registers = tuple[Register, Register, Register, Register] | list[Register]
Operation = Callable[[Registers, Input, Input, Output], Registers]


@dataclass(frozen=True)
class Trace:
    """
    Holds information about a single observed instruction
    """
    instruction: Instruction
    pre: Registers
    post: Registers


def opcode(func: Operation) -> Operation:
    """
    Decorator to handle common logic in processing opcodes
    """
    def wrapper(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> Registers:
        """
        Handle pre and post-processing for Operations
        """
        pre: list[int] = list(pre)
        func(self, pre, input1, input2, output)
        return tuple(pre)

    return wrapper


class Emulator:
    """
    Emulator for device opcodes
    """
    def __init__(self) -> None:
        """
        Get the list of opcode methods
        """
        self.operations: dict[str, Operation] = {
            item[0]: item[1]
            for item in inspect.getmembers(self, inspect.ismethod)
            if not item[0].startswith('_')
        }

    @opcode
    def addr(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        addr: add register
        """
        pre[output] = pre[input1] + pre[input2]

    @opcode
    def addi(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        addi: add immediate
        """
        pre[output] = pre[input1] + input2

    @opcode
    def mulr(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        mulr: multiply register
        """
        pre[output] = pre[input1] * pre[input2]

    @opcode
    def muli(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        muli: multiply immediate
        """
        pre[output] = pre[input1] * input2

    @opcode
    def banr(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        banr: bitwise AND register
        """
        pre[output] = pre[input1] & pre[input2]

    @opcode
    def bani(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        bani: bitwise AND immediate
        """
        pre[output] = pre[input1] & input2

    @opcode
    def borr(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        borr: bitwise OR register
        """
        pre[output] = pre[input1] | pre[input2]

    @opcode
    def bori(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        bori: bitwise OR immediate
        """
        pre[output] = pre[input1] | input2

    @opcode
    def setr(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,  # pylint: disable=unused-argument
        output: Output,
    ) -> None:
        """
        setr: assign register

        Copies contents of register specified by "input1" param into the
        register specified by the "output" param. "input2" is ignored.
        """
        pre[output] = input1

    @opcode
    def seti(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,  # pylint: disable=unused-argument
        output: Output,
    ) -> None:
        """
        setr: assign immediate

        Copies value of the "input1" param into the register specified by the
        "output" param. "input2" is ignored.
        """
        pre[output] = pre[input1]

    @opcode
    def gtir(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        gtir: greater-than immediate/register

        sets register number specified by the "output" param to 1 if the value
        of the "input1" param is greater than the value stored in the register
        specified by the "input2" param. Otherwise, the output is set to 0.
        """
        pre[output] = 1 if input1 > pre[input2] else 0

    @opcode
    def gtri(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        gtri: greater-than register/immediate

        sets register number specified by the "output" param to 1 if the value
        stored in the register specified by the "input1" param is greater than
        the value of the "input2" param. Otherwise, the output is set to 0.
        """
        pre[output] = 1 if pre[input1] > input2 else 0

    @opcode
    def gtrr(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        gtrr: greater-than register/register

        sets register number specified by the "output" param to 1 if the value
        stored in the register specified by the "input1" param is greater than
        the value stored in the register specfied by the the "input2" param.
        Otherwise, the output is set to 0.
        """
        pre[output] = 1 if pre[input1] > pre[input2] else 0

    @opcode
    def eqir(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        eqir: equal immediate/register

        sets register number specified by the "output" param to 1 if the value
        of the "input1" param is equal to the value stored in the register
        specified by the "input2" param. Otherwise, the output is set to 0.
        """
        pre[output] = 1 if input1 == pre[input2] else 0

    @opcode
    def eqri(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        eqri: equal register/immediate

        sets register number specified by the "output" param to 1 if the value
        stored in the register specified by the "input1" param is equal to
        the value of the "input2" param. Otherwise, the output is set to 0.
        """
        pre[output] = 1 if pre[input1] == input2 else 0

    @opcode
    def eqrr(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,
        output: Output,
    ) -> None:
        """
        eqrr: equal register/register

        sets register number specified by the "output" param to 1 if the value
        stored in the register specified by the "input1" param is equal to
        the value stored in the register specfied by the the "input2" param.
        Otherwise, the output is set to 0.
        """
        pre[output] = 1 if pre[input1] == pre[input2] else 0


class AOC2018Day16(AOC):
    """
    Day 16 of Advent of Code 2018
    """
    example_data: str = textwrap.dedent(
        """
        Before: [3, 2, 1, 1]
        9 2 1 2
        After:  [3, 2, 2, 1]
        """
    )

    validate_part1: int = 1

    emu: Emulator = Emulator()

    # Set by post_init (or elsewhere)
    traces = None
    program = None

    def post_init(self) -> None:
        """
        Load the CPU trace results
        """
        self.traces: list[Trace] = []

        trace: tuple[str, ...]

        for trace in re.findall(
            r"Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]\n"
            r"(\d+) (\d+) (\d+) (\d+)\n"
            r"After:\s+\[(\d+), (\d+), (\d+), (\d+)\]",
            self.input,
            flags=re.MULTILINE,
        ):
            self.traces.append(
                Trace(
                    instruction=tuple(int(n) for n in trace[4:8]),
                    pre=tuple(int(n) for n in trace[:4]),
                    post=tuple(int(n) for n in trace[8:]),
                )
            )

        try:
            # Isolate the program at the bottom of the input and convert the
            # strings to integers, storing them in a sequence of tuples.
            self.program: Program = tuple(
                tuple(int(n) for n in line.split())
                for line in self.input.split("\n\n\n\n")[1].strip().splitlines()
            )
        except IndexError:
            # The example input has no program
            self.program: Program = ()

    def part1(self) -> int:
        """
        Return the number of traces which behave like three or more opcodes
        """
        trace: Trace
        operation: Operation

        ret: int = 0

        for trace in self.traces:
            matches: int = 0
            for operation in self.emu.operations.values():
                if operation(trace.pre, *trace.instruction[1:]) == trace.post:
                    matches += 1
                    if matches == 3:
                        ret += 1
                        # We know this matches at least 3 operations, no need
                        # to check further
                        break

        return ret

    def part2(self) -> int:
        """
        Figure out which opcode belongs to which number. Then, run the program
        from the puzzle input and return the value of register 0 at the end of
        execution.
        """
        if not self.program:
            raise RuntimeError("Failed to parse program from input")

        # Create a mapping of opcode names to potential matching numbers
        operation_map: dict[OpcodeName, set[OpcodeNumber]] = defaultdict(set)
        for trace in self.traces:
            for name, operation in self.emu.operations.items():
                if operation(trace.pre, *trace.instruction[1:]) == trace.post:
                    operation_map[name].add(trace.instruction[0])

        # Maps opcode numbers to the function from the emulator. Once all
        # opcodes have been mapped, this dict will be used to run the program.
        opcode_map: dict[OpcodeNumber, Operation] = {}

        # By process of elimination, determine which operations correspond to
        # which opcodes.
        while operation_map:
            # Get all operations which only map to a single opcode number,
            # these have been narrowed down and we now know the operation
            # corresponding to these numbers.
            singles: dict[OpcodeNumber, OpcodeName] = {
                list(val)[0]: key for key, val in operation_map.items()
                if len(val) == 1
            }
            if not singles:
                raise RuntimeError("No singles found!")

            # Update the opcode map with the items we found above
            opcode_map.update({
                key: self.emu.operations[val]
                for key, val in singles.items()
            })

            # Remove references to the opcodes discovered above
            known_codes: frozenset[OpcodeNumber] = frozenset(singles)
            name: OpcodeName
            for name in list(operation_map):
                # Remove references to the known opcodes
                operation_map[name] -= known_codes
                # If no opcode numbers are left corresponding to this opcode
                # name, we know this operation's opcode number and can remove
                # it from the operation_map.
                if not operation_map[name]:
                    del operation_map[name]

        # Initialize all registers to 0
        registers: Registers = (0, 0, 0, 0)

        # Run the program using the mapping of opcodes to operations which we
        # determined in the loop above
        instruction: Instruction
        for instruction in self.program:
            registers = opcode_map[instruction[0]](registers, *instruction[1:])

        # Return the contents of register 0
        return registers[0]


if __name__ == '__main__':
    aoc = AOC2018Day16()
    aoc.run()
