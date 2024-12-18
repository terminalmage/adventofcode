#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/17
'''
import itertools
import re
import textwrap
from dataclasses import dataclass
from typing import Literal

# Local imports
from aoc import AOC

# Type hints
Code = Literal['0', '1', '2', '3', '4', '5', '6', '7']
Program = tuple[Code, ...]
Output = tuple[int, ...]


@dataclass
class Computer:
    '''
    Simulates a computer, with its three registers
    '''
    program: Program
    a: int = 0
    b: int = 0
    c: int = 0

    def init(self, **init: int) -> None:
        '''
        Reset registers and use any kwargs passed in to set initial values
        '''
        register: str
        value: int

        # Reset all registers to 0
        self.a = self.b = self.c = 0
        # Set initial values
        for register, value in init.items():
            setattr(self, register, value)

    def run(self, **init: int) -> Output:
        '''
        Run the program passed in. The return will be the output of the
        program, expressed as a tuple of ints.
        '''
        self.init(**init)

        # Index of where we are in the program's instruction set
        index: int = 0

        def _combo(val: int) -> int:
            '''
            Interpret the value of the combo operand
            '''
            match val:
                case 0 | 1 | 2 | 3:
                    return val
                case 4:
                    return self.a
                case 5:
                    return self.b
                case 6:
                    return self.c
                case _:
                    raise ValueError('Invalid combo operand')

        outputs: list[int] = []

        opcode: int
        operand: int
        while True:
            try:
                opcode, operand = self.program[index:index + 2]
            except (IndexError, ValueError):
                return tuple(outputs)

            match opcode:
                # opcode 0: adv
                #   divide register a by 2^operand
                case 0:
                    self.a //= 2 ** _combo(operand)

                # opcode 1: bxl
                #   bitwise XOR on register b
                case 1:
                    self.b ^= operand

                # opcode 2: bst
                #   stores lowest 3 bits of operand mod 8 to register b
                case 2:
                    self.b = _combo(operand) % 8

                # opcode 3: jnz
                #   set instruction pointer to the value in the operand if register
                #   a is set to a nonzero value
                case 3:
                    if self.a:
                        index = operand
                        continue

                # opcode 4: bxc
                #   perform a bitwise XOR on registers b and c, storing the
                #   result in register b. Operand is ignored.
                case 4:
                    self.b ^= self.c

                # opcode 5: out
                #   Output the value of the operand mod 8
                case 5:
                    outputs.append(_combo(operand) % 8)

                # opcode 6: bdv
                #   works the same as adv but stores result in register b
                case 6:
                    self.b = self.a // (2 ** _combo(operand))

                # opcode 6: cdv
                #   works the same as adv but stores result in register c
                case 7:
                    self.c = self.a // (2 ** _combo(operand))

                case _:
                    raise ValueError(f'Invalid opcode: {opcode}')

            index += 2


class AOC2024Day17(AOC):
    '''
    Day 17 of Advent of Code 2024
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        Register A: 729
        Register B: 0
        Register C: 0

        Program: 0,1,5,4,3,0
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        Register A: 2024
        Register B: 0
        Register C: 0

        Program: 0,3,5,4,3,0
        '''
    )

    validate_part1: str = '4,6,3,5,6,3,5,2,1,0'
    validate_part2: int = 117440

    def parse_input(self, puzzle_input: str):
        '''
        Get all the integers from the input. The first 3 encountered will be
        the starting values of the registers, while the remaining ones
        represent the program.
        '''
        numbers = map(int, re.findall(r'\d+', puzzle_input))
        registers: dict[str, int] = dict(
            zip('abc', itertools.islice(numbers, 3))
        )
        computer = Computer(tuple(numbers))
        return registers, computer

    def part1(self) -> str:
        '''
        Return the output of the program given the starting values of the
        registers as defined in the puzzle input.
        '''
        registers, computer = self.parse_input(self.input_part1)
        return ','.join(map(str, computer.run(**registers)))

    def part2(self) -> int:
        '''
        The example program from Part 2: 0,3,5,4,3,0

        Register A starts with the solution: 117440

        This results in the following actions:

        1. 0,3  (adv 3)  a //= 2^3

            - Dividing by 2^N is the same as shifting N bits to the right
            - a //= 2^3 is the same as a >> 3
            - 117440 >> 3 = 14680

        2. 5,4  (out 4)  output a % 8

            - 14680 % 8 = 0

        3. 3,0  (jnz 0)  sets instruction pointer to 0 (beginning of program)

        Due to the jumps, this results in a loop which repeats until a == 0,
        resulting in the following:

            117440 >> 3 = 14680
            output 14680 % 8 (0)
            14680 >> 3 = 1835
            output 1835 % 8 (3)
            1835 >> 3 = 229
            output 229 % 8 (5)
            229 >> 3 = 28
            output 28 % 8 (4)
            28 >> 3 = 3
            output 3 % 8 (3)
            3 >> 3 = 0
            output 0 % 8 (0)

        The sequence of numbers which is output is the same sequence as the
        program itself.

        After the last output, register A equals 0, so the jnz opcode does not
        jump, and the program ends.

        The key to applying this to the real puzzle input is that all of the
        programs will shift A by 3 bits each time through the loop. What
        happens after that, and what gets output, varies from one unique
        program input to the next, but every program will systematically shift
        the value of A by 3 bits until it reaches 0.

        To reverse-engineer which values of register A will produce a copy of
        the program as output, we need to reverse this process.

            - The program decreases the value of the register as it produces
              digits from left to right. So we need to increase the number as
              we move right to left.

            - The program divides by 8 (i.e. shifts three bits right) and the
              output is the remainder. To reverse this we need to guess a
              remainder, and multiply by 8 (i.e. shift three bits left).

            - Think of this like building a base-N number from right to left.
              The rightmost column is some number multiplied by N^0, the next
              column to the left is a number multiplied by N^1, etc.
        '''
        computer: Computer
        _, computer = self.parse_input(self.input_part2)

        # Start with every possible N*8^0 value. This will represent all of our
        # guesses for what produces a remainder of 0 (i.e. the rightmost digit
        # in the program).
        possible = set(range(8))

        # Continue with trying to make the second-rightmost number, then the
        # third-rightmost, and so on. As we proceed through this loop, we will
        # be growing a group of numbers that produce ever-growing subsets of
        # the program's digits. To represent this algorithmically, we will use
        # negative slicing of the digits in the program. So, on the first pass
        # we will be looking at program[-2:], the second pass will be
        # program[-3:], until at last we are looking at the entire program.
        # Originally I had an off-by-one error that I still don't understand
        # the explanation for. I thought that this process would be done when
        # the subset of the string we are looking at is the entire string (i.e.
        # program[-len(program):]). I'm still not quite sure why it needs an
        # extra pass, since the final two passes will have an identical target
        # (that is, p[-len(p):] and p[-len(p)-1:] are identical slices). But
        # the answer I came up with ended up being off by a factor of 8, so I
        # assumed it was an off-by-one error and added another pass, and ended
        # up with the correct answer.
        for size in range(2, len(computer.program) + 1):
            # Get the subset of the program we are focusing on
            target = computer.program[-size:]

            # Grow our possible solutions by taking each number from the
            # "possible" set and then performing the reverse (i.e. multiply by
            # 8/shift by 3 bits, then add the guessed remainder). Keep only the
            # combinations that, when the entire program is run, produce the
            # targeted subset of the program. Trying each combination can be
            # expressed very elegantly in a set comprehension.
            possible = {
                (item << 3) + n
                for item in possible
                for n in range(8)
                if computer.run(a=(item << 3) + n) == target
            }

        # This set will contain all the possible starting register A values
        # which produce the desired output. Per the puzzle description, we need
        # the lowest value.
        return min(possible)


if __name__ == '__main__':
    aoc = AOC2024Day17()
    aoc.run()
