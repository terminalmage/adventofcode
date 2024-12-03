#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/3
'''
import math
import re
import textwrap
from collections.abc import Iterator, Sequence

# Local imports
from aoc import AOC


class AOC2024Day3(AOC):
    '''
    Day 3 of Advent of Code 2024
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
        '''
    )
    example_data_part2: str = textwrap.dedent(
        '''
        xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
        '''
    )

    validate_part1: int = 161
    validate_part2: int = 48

    @staticmethod
    def solve(pairs: Sequence[tuple[str, str]]) -> int:
        '''
        Given a sequence of operand pairs (captured as strings from a regex),
        convert them to integer pairs, multiply each pair, and return the sum
        of the resulting products.
        '''
        return sum(math.prod(map(int, pair)) for pair in pairs)

    def part1(self) -> int:
        '''
        Return the sum of all non-corrupted mul() instructions
        '''
        return self.solve(re.findall(r"mul\((\d+),(\d+)\)", self.input_part1))

    def part2(self) -> int:
        '''
        Return the sum of all *enabled* non-corrupted mul() instructions
        '''
        def _find_enabled() -> Iterator[int]:
            '''
            Yields a sequence of enabled mul statements
            '''
            enabled: bool = True
            pat_match: re.Match
            for pat_match in re.finditer(
                r"mul\((\d+),(\d+)\)|(do(?:n't)?)\(\)",
                self.input_part2,
            ):
                match pat_match.group(3):
                    case "do":
                        enabled = True
                    case "don't":
                        enabled = False
                    case _:
                        if enabled:
                            yield pat_match.groups()[:2]

        return self.solve(_find_enabled())


if __name__ == '__main__':
    aoc = AOC2024Day3()
    aoc.run()
