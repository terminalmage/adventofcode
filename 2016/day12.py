#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/12
'''
import copy
import re
from dataclasses import dataclass

# Local imports
from aoc import AOC

Instruction = str
Program = list[Instruction]


@dataclass
class Computer:
    '''
    Simulates a computer, with its four registers
    '''
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0

    def reset(self) -> None:
        '''
        Reset all the registers' values to 0
        '''
        self.a = self.b = self.c = self.d = 0

    def init(self, **init: int) -> None:
        '''
        Reset registers and use any kwargs passed in to set initial values
        '''
        register: str
        value: int

        # Reset all registers to 0
        self.reset()
        # Set initial values
        for register, value in init.items():
            setattr(self, register, value)

    def resolve(self, value: str) -> int:
        '''
        Given a string, return either the value of the matching register, or
        failing that, assume it's a string integer and return the result.
        '''
        try:
            return getattr(self, value)
        except AttributeError:
            return int(value)

    def optimize(self, program: Program) -> Program:  # pylint: disable=too-many-statements
        '''
        Detect loops and optimize them. For example, consider the following
        sequence of instructions:

            cpy b c
            inc a
            dec c
            jnz c -2
            dec d
            jnz d -5

        The result of this loop will be to multiply the values in registers b
        and d, add the result to register a, and zero out both registers c and
        d. We know this because we execute the outer loop until d == 0 (in
        other words, "d" times), and each time we do so, we take the value from
        register b, load it into register c, and increment register a until
        register c is zero.

        After optimizing double loops, look for and optimize single loops. They
        will look like the following:

            dec d
            inc c
            jnz d -2

        This will have the result of increasing the value of register c by the
        value of register d, and zeroing out register d.
        '''
        # Make shallow copy of program since we will be modifying its
        # instructions in place.
        program: Program = copy.copy(program)

        double_loop: re.Pattern = re.compile(r'^jnz ([bcd]) -5$')
        single_loop: re.Pattern = re.compile(r'^jnz ([bcd]) -2$')

        index: int
        instruction: Instruction

        # Detect and optimize double loops
        for index, instruction in enumerate(program):
            try:
                outer_reg: str = double_loop.match(instruction).group(1)
            except AttributeError:
                # Regex did not match
                continue
            # Sanity check and make sure this fits the optimization pattern
            # (i.e. the same register from the jnz is being decremented each
            # iteration of the outer loop)
            if program[index - 1] != f'dec {outer_reg}':
                continue
            # Now that we've confirmed the outer loop pattern, check for the
            # inner loop.
            cmd: str
            inner_reg: str
            temp_reg: str
            try:
                cmd, inner_reg, temp_reg = program[index - 5].split()
            except ValueError:
                continue
            if cmd != 'cpy':
                continue
            # If we've gotten here, we know that the inner_reg is being copied
            # into the temp_reg each iteration of the outer loop. Confirm that
            # the other commands match the inner loop pattern.
            if program[index - 3:index - 1] != [
                f'dec {temp_reg}',
                f'jnz {temp_reg} -2',
            ]:
                continue
            # Finally, confirm the register that will be increased by this loop
            action: str
            mod_reg: str
            try:
                action, mod_reg = program[index - 4].split()
            except ValueError:
                continue
            if action not in ('inc', 'dec'):
                continue
            # We've now confirmed the structure of the inner and outer loops
            # and can construct our optimized command. We will place it at
            # index - 5 and then overwrite the other commands from the loop
            # with "jnz 0 0" which will A) be no-ops and B) preserve the total
            # number of commands (in case the logic and register positions
            # dictate that the loop should be jumped around using a jnz).
            program[index - 5] = (
                f'mul {inner_reg} {outer_reg} {action} {mod_reg} '
                f'clear {temp_reg}{outer_reg}'
            )
            for i in range(index - 4, index + 1):
                program[i] = 'jnz 0 0'

        # Detect and optimize single loops
        for index, instruction in enumerate(program):
            try:
                temp_reg: str = single_loop.match(instruction).group(1)
            except AttributeError:
                # Regex did not match
                continue
            # Look at the previous two instructions and make sure we have an
            # instruction which decrements that register
            prev: list[Instruction] = program[index - 2:index]
            try:
                prev.remove(f'dec {temp_reg}')
            except ValueError:
                continue
            # Detect the other instruction
            action: str
            mod_reg: str
            try:
                action, mod_reg = prev[0].split()
            except ValueError:
                continue
            if action not in ('inc', 'dec'):
                continue
            # We've now confirmed that this matches the characteristics of a
            # single loop. Like we did for double-loops, modify the program and
            # inject an optimized command.
            program[index - 2] = f'trans {temp_reg} {action} {mod_reg}'
            for i in range(index - 1, index + 1):
                program[i] = 'jnz 0 0'

        return program

    def exec(self, index: int, instruction: Instruction) -> int:
        '''
        Execute the specified instruction, and return the index of the next
        instruction to be run.
        '''
        match instruction.split():
            case ['cpy', value, register]:
                value: int
                try:
                    value = int(value)
                except ValueError:
                    # Value is not an int, but rather another register
                    value = getattr(self, value)
                # Set register to the desired value
                setattr(self, register, value)

            case ['inc', register]:
                # Increment register
                setattr(self, register, getattr(self, register) + 1)

            case ['dec', register]:
                # Decrement register
                setattr(self, register, getattr(self, register) - 1)

            case ['jnz', register, value]:
                # Jump forward/backward by the specified number of
                # instructions, but only if the specified register does not
                # contain a value of 0. If the register is not found, it is
                # assumed that the parameter directly after the 'jnz' is an
                # integer value rather than the name of a register.
                register_value: int = self.resolve(register)

                # Jump forward/backward if the value is > 0
                if register_value:
                    return index + self.resolve(value)

            # The following two commands are not part of the instruction set,
            # but are rather added by the loop optimization logic.

            case ['mul', reg1, reg2, action, mod_reg, 'clear', clear]:
                # Multiply the two specified registers
                product: int = self.resolve(reg1) * self.resolve(reg2)
                if action == 'dec':
                    product *= -1
                # Add the product to the register we are modifying
                setattr(self, mod_reg, getattr(self, mod_reg) + product)
                # Clear the specified register(s)
                clear_reg: str
                for clear_reg in clear:
                    setattr(self, clear_reg, 0)

            case ['trans', reg1, action, reg2]:
                # Transfer the value from reg1 into reg2, clearing reg1
                value: int = self.resolve(reg1)
                if action == 'dec':
                    value *= -1
                setattr(self, reg2, getattr(self, reg2) + value)
                # Clear reg1
                setattr(self, reg1, 0)

            case _:
                raise ValueError(f'Invalid command: {instruction!r}')

        # The new index will be the next instruction, unless we jumped above.
        return index + 1

    def run(self, program: Program, **init: int) -> None:
        '''
        Run the program passed in
        '''
        # Apply any initial values passed in
        self.init(**init)

        # Index of where we are in the program's instruction set
        index: int = 0

        # Detect and optimize loops
        program: Program = self.optimize(program)

        while index < len(program):
            index = self.exec(index, program[index])


class AOC2016Day12(AOC):
    '''
    Day 12 of Advent of Code 2016
    '''
    day = 12

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the computer and load the program from the puzzle input
        '''
        super().__init__(example=example)
        self.computer: Computer = Computer()
        self.program: Program = self.input.read_text().splitlines()

    def part1(self) -> int:
        '''
        Return the value in register a after the program runs to completion
        '''
        self.computer.run(self.program)
        return self.computer.a

    def part2(self) -> int:
        '''
        Same as part 1, but with register c initialized to 1
        '''
        self.computer.run(self.program, c=1)
        return self.computer.a


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day12(example=True)
    aoc.validate(aoc.part1(), 42)
    # Run against actual data
    aoc = AOC2016Day12(example=False)
    aoc.run()
