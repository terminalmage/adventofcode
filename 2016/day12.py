#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/12
'''
from dataclasses import dataclass

# Local imports
from aoc import AOC

Instruction = str
Program = tuple[Instruction, ...]


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

    def run(self, program: Program, **init: int) -> None:
        '''
        Run the program passed in
        '''
        # Reset all registers to 0
        self.reset()

        # Apply any initial values passed in
        register: str
        value: int
        for register, value in init.items():
            setattr(self, register, value)

        # Index of where we are in the program's instruction set
        index: int = 0

        while index < len(program):
            match program[index].split():
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
                    register_value: int
                    try:
                        register_value = getattr(self, register)
                    except AttributeError:
                        register_value = int(register)

                    # Jump forward/backward if the value is > 0
                    if register_value:
                        index += int(value)
                        # Skip to next instruction
                        continue

                case _:
                    raise ValueError(f'Invalid command: {program[index]!r}')

            # Increment the index by one, unless we jumped above
            index += 1


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
        self.program: Program = tuple(self.input.read_text().splitlines())

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
