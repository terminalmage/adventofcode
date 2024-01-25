#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/25
'''
from __future__ import annotations
import functools
import re
import textwrap

# Local imports
from aoc import AOC


class SNAFU:
    '''
    Represents a single SNAFU number
    '''
    def __init__(self, value: str | int) -> None:
        '''
        Initialize the SNAFU number. Can be initialized from a base 10 integer
        or from SNAFU notation.
        '''
        # Load internally as an integer for ease of computation
        self.value: int
        if isinstance(value, int):
            self.value = value
        else:
            try:
                if not re.match(r'[012=-]+', value):
                    raise ValueError('Invalid SNAFU-notation string')
            except TypeError as exc:
                raise TypeError(
                    'Must be an integer or SNAFU-notation string'
                ) from exc
            self.value = self.__to_int(value)

    def __str__(self) -> str:
        '''
        Returns the SNAFU notation for the number
        '''
        def __to_str(value):
            if value == 0:
                return ''

            match value % 5:
                case 0 | 1 | 2:
                    return __to_str(value // 5) + str(value % 5)
                case 3:
                    return __to_str((value // 5) + 1) + '='
                case 4:
                    return __to_str((value // 5) + 1) + '-'

        if self.value == 0:
            return str(self.value)

        return __to_str(self.value)

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'SNAFU({self.__str__()!r}, int={self.value})'

    @staticmethod
    def __to_int(value: str) -> int:
        '''
        Convert SNAFU notation to integer
        '''
        ceiling: int = 5**len(value)
        ret: int = 0
        col: str
        for col in value:
            ceiling //= 5
            match col:
                case '1' | '2':
                    ret += ceiling * int(col)
                case '=':
                    ret -= ceiling * 2
                case '-':
                    ret -= ceiling
        return ret

    def __add__(self, other: SNAFU) -> SNAFU:
        '''
        Add two different SNAFU objects, returning a new SNAFU object
        '''
        if not isinstance(other, SNAFU):
            raise TypeError(
                f'Unsupported operand type(s) for +: '
                f'{type(self).__name__!r} and '
                f'{type(other).__name__!r}'
            )
        return SNAFU(self.value + other.value)

    def __iadd__(self, other: SNAFU) -> SNAFU:
        '''
        Add two different SNAFU objects, updating the instance's value
        '''
        if not isinstance(other, SNAFU):
            raise TypeError(
                f'Unsupported operand type(s) for +: '
                f'{type(self).__name__!r} and '
                f'{type(other).__name__!r}'
            )
        self.value += other.value
        return self


class AOC2022Day25(AOC):
    '''
    Day 25 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        1=-0-2
        12111
        2=0=
        21
        2=01
        111
        20012
        112
        1=-1=
        1-12
        12
        1=
        122
        '''
    )

    validate_part1: str = '2=-1=0'

    def post_init(self) -> None:
        '''
        Load the numbers from the input file
        '''
        self.numbers = tuple(
            SNAFU(line)
            for line in self.input.splitlines()
        )

    def part1(self) -> str:
        '''
        Add up all the SNAFU numbers and report the result in SNAFU notation
        '''
        return str(functools.reduce(lambda x, y: x + y, self.numbers))


if __name__ == '__main__':
    aoc = AOC2022Day25()
    aoc.run()
