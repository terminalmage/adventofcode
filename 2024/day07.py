#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/7
'''
import itertools
import re
import textwrap
from collections.abc import Iterator, Sequence
from typing import Callable

# Local imports
from aoc import AOC

# Type hints
Result = Operand = int
Operands = tuple[Operand, ...]
Equation = tuple[Result, Operands]
Operator = Callable[[int, int], int]


class AOC2024Day7(AOC):
    '''
    Day 7 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
        '''
    )

    validate_part1: int = 3749
    validate_part2: int = 11387

    @property
    def equations(self) -> Iterator[Equation]:
        '''
        Generator that returns one equation at a time from the input
        '''
        for line in self.input.splitlines():
            ints: list[int] = list(map(int, re.findall(r'\d+', line)))
            yield (ints[0], ints[1:])

    @staticmethod
    def is_valid(
        result: Result,
        operands: Operands,
        operators: Sequence[Operator] = (int.__mul__, int.__add__),
    ) -> bool:
        '''
        Return True for a valid equation, otherwise False
        '''
        # Get all possible sequences of operators
        operator_sequence: tuple[Operator, ...]
        for operator_sequence in itertools.product(
            operators,
            repeat=len(operands) - 1
        ):
            total: Operand = operands[0]
            operator: Operator
            operand: Operand
            for operator, operand in zip(operator_sequence, operands[1:]):
                total = operator(total, operand)

            if total == result:
                return True

        return False

    def part1(self) -> int:
        '''
        Return the number of valid equations based on the criteria from Part 1
        '''
        return sum(
            result for result, operands in self.equations
            if self.is_valid(result, operands)
        )

    def part2(self) -> int:
        '''
        Return the number of valid equations based on the criteria from Part 2
        '''
        return sum(
            result for result, operands in self.equations
            if self.is_valid(
                result,
                operands,
                operators=(int.__mul__, int.__add__, lambda x, y: int(str(x) + str(y))),
            )
        )


if __name__ == '__main__':
    aoc = AOC2024Day7()
    aoc.run()
