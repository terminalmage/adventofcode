#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/13
'''
import re
import textwrap
from dataclasses import dataclass
from collections.abc import Iterator

# Local imports
from aoc import AOC, MathMixin


@dataclass
class ClawMachine:
    '''
    Represents a claw machine definition from the puzzle input, for example:

    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400
    '''
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int


class AOC2024Day13(AOC, MathMixin):
    '''
    Day 13 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400

        Button A: X+26, Y+66
        Button B: X+67, Y+21
        Prize: X=12748, Y=12176

        Button A: X+17, Y+86
        Button B: X+84, Y+37
        Prize: X=7870, Y=6450

        Button A: X+69, Y+23
        Button B: X+27, Y+71
        Prize: X=18641, Y=10279
        '''
    )

    validate_part1: int = 480

    @property
    def machines(self) -> Iterator[ClawMachine]:
        '''
        Iterate over the input and yield a ClawMachine dataclass instance for
        each claw machine definition.
        '''
        machine_def: str
        for machine_def in self.input.split('\n\n'):
            yield ClawMachine(*map(int, re.findall(r'\d+', machine_def)))

    def solve(self, offset: int = 0):
        '''
        Calculate the number of tokens you would need to spend to win each game
        (for which a possible solution exists).

        The input can be represented as a system of linear equations. For
        example, take the following from the example input:

        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400

        This can be written as the following two equations:

            94A + 22B = 8400
            34A + 67B = 5400

        This is a system of two linear equations with two unknowns, and it can
        be solved using Cramer's Rule.
        '''
        ret: int = 0
        machine: ClawMachine
        for machine in self.machines:
            A: float
            B: float
            A, B = self.cramer_2x2(
                a1=machine.ax,
                b1=machine.bx,
                c1=machine.px + offset,
                a2=machine.ay,
                b2=machine.by,
                c2=machine.py + offset,
            )
            # if either A or B is not an integer, then it is not possible to
            # win the game with any combination of A and B button presses.
            # Since A and B are the result of integer division, they will come
            # back as float types. Use the .is_integer() method from the float
            # data type to confirm that both are integers.
            if A.is_integer() and B.is_integer():
                ret += int((3 * A) + B)

        return ret

    def part1(self) -> int:
        '''
        Return the number of tokens needed to win all the winnable games
        '''
        return self.solve()

    def part2(self) -> int:
        '''
        Return the number of tokens needed to win all the winnable games, with
        the X and Y locations of the prizes adjusted by the specified offset.
        '''
        return self.solve(offset=10_000_000_000_000)


if __name__ == '__main__':
    aoc = AOC2024Day13()
    aoc.run()
