#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/15
'''
import itertools
import textwrap
from collections.abc import Generator

# Local imports
from aoc import AOC

# Type hints
NumberGen = Generator[int, None, None]


class AOC2017Day15(AOC):
    '''
    Day 15 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        Generator A starts with 65
        Generator B starts with 8921
        '''
    )

    validate_part1: int = 588
    validate_part2: int = 309

    def post_init(self) -> None:
        '''
        Load the puzzle input
        '''
        self.seed_a: int
        self.seed_b: int
        self.seed_a, self.seed_b = (
            int(line.split()[-1]) for line in self.input.splitlines()
        )

    @staticmethod
    def number_gen(
        seed: int,
        multiplier: int,
        divisible_by: int = 1
    ) -> NumberGen:
        '''
        Given a seed and multiplier value, return a generator matching the
        parameters stated in the puzzle description.
        '''
        while True:
            seed = (seed * multiplier) % 2147483647
            if not seed % divisible_by:
                yield seed

    @staticmethod
    def matches(
        gen_a: NumberGen,
        gen_b: NumberGen,
        pairs: int,
    ) -> int:
        '''
        Given two number generators, generate the specified number of pairs,
        and return the number of pairs which share the rightmost 16 bits.

        In Python, the result of a bitwise operation only considers the bits up
        to the bit length of the rvalue. Therefore, for each pair we can
        perform a bitwise AND using a 16-bit number containing all 1s (i.e.
        0xffff). An AND is used because it returns 1 if both bits are 1,
        otherwise 0. Thus, AND'ing with all 1s will have the effect of giving
        you an int containing only the the rightmost 16 bits, since an AND
        yields 1 when both bits match, and 0 when they do not. If the bitwise
        AND results for both numbers in a given pair are equal, then we know
        the last 16 bits are the same, and can count that pair as a match.
        '''
        num_a: int
        num_b: int
        matches: int = 0

        for num_a, num_b in itertools.islice(zip(gen_a, gen_b), 0, pairs):
            if num_a & 0xffff == num_b & 0xffff:
                matches += 1

        return matches

    def part1(self) -> int:
        '''
        Return the number of matches using the criteria from Part 1
        '''
        return self.matches(
            self.number_gen(self.seed_a, 16807),
            self.number_gen(self.seed_b, 48271),
            40_000_000,
        )

    def part2(self) -> int:
        '''
        Return the number of matches using the criteria from Part 2
        '''
        return self.matches(
            self.number_gen(self.seed_a, 16807, divisible_by=4),
            self.number_gen(self.seed_b, 48271, divisible_by=8),
            5_000_000,
        )


if __name__ == '__main__':
    aoc = AOC2017Day15()
    aoc.run()
