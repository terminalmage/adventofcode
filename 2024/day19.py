#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/19
'''
import functools
import textwrap

# Local imports
from aoc import AOC

# Type hints
Towel = str
Towels = tuple[Towel, ...]
Design = str
Designs = tuple[Design, ...]


@functools.cache
def check_design(design: Design, towels: Towels) -> int:
    '''
    Recursive function to check which (if any) combination of patterns can make
    the specified design. Returns the number of matches that can be made.

    This works by finding all towels that can match the beginning of a design,
    then recursing and finding all towels that can match the beginning of the
    remainder of the design, and continuing recursion until there is nothing
    left to match. The function then returns 1 to signify that a match for the
    full design has been reached.

    Each recursive call keeps a tally of the times a full match was reached
    under it, returning that value after it has checked every towel against its
    subset of the design. The result is that each level of recursion returns
    the number of full matches accumulated underneath it, and the original call
    returns the total number of possible calls.

    Memoization is used to prevent duplicated effort.
    '''
    if not design:
        # We've recursed to the point that there is nothing else to match, so
        # this is a match.
        return 1

    combos: int = 0

    towel: Towel
    for towel in (x for x in towels if design.startswith(x)):
        combos += check_design(design[len(towel):], towels)

    return combos


class AOC2024Day19(AOC):
    '''
    Day 19 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        r, wr, b, g, bwu, rb, gb, br

        brwrr
        bggr
        gbbr
        rrbgbr
        ubwu
        bwurrg
        brgr
        bbrgwb
        '''
    )

    validate_part1: int = 6
    validate_part2: int = 16

    # Set by post_init
    towels = None
    designs = None

    def post_init(self) -> None:
        '''
        Load the puzzle data
        '''
        towels: str
        designs: str
        towels, designs = self.input.split('\n\n')
        self.towels: Towels = tuple(towels.replace(',', '').split())
        self.designs: Designs = tuple(designs.splitlines())

    def part1(self) -> int:
        '''
        Return the number of designs which have at least one possible towel
        combination that can be used to make them.

        True has a value of 1 when coerced to an int, while False has a value
        of 0. sum() attempts to coerce non-numeric types into ints, so the
        result is that sum() increments the result by 1 for each True value
        (i.e. each design that has at least one possible match).
        '''
        return sum(
            bool(check_design(design, self.towels))
            for design in self.designs
        )

    def part2(self) -> str:
        '''
        Return all possible combinations. Memoization makes this super fast, as
        all the work was done in Part 1 and the check_design() func already has
        the answer.
        '''
        return sum(
            check_design(design, self.towels)
            for design in self.designs
        )


if __name__ == '__main__':
    aoc = AOC2024Day19()
    aoc.run()
