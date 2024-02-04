#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/18
'''
import textwrap
from typing import Literal

# Local imports
from aoc import AOC

SAFE = '0'
TRAP = '1'

# Typing shortcuts
Tile = Literal[SAFE, TRAP]


class AOC2016Day18(AOC):
    '''
    Day 18 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        .^^.^.^^^^
        '''
    )

    validate_part1: int = 38

    # Set by post_init
    first_line = None

    def post_init(self) -> None:
        '''
        Load the puzzle data
        '''
        # A "0" represents a safe tile, while a "1" represents a trap. For an
        # explanation of why, see the docstring for the "rule90" method below.
        trans: dict[int, int] = str.maketrans('.^', '01')
        self.first_line: str = self.input.translate(trans)

    def rule90(self, num_lines: int) -> int:
        '''
        Return the number of "safe" tiles in the specified number of lines,
        given the replication pattern defined in the puzzle input.

        The puzzle describes the Rule 90 cellular automataion:

            https://en.wikipedia.org/wiki/Rule_90

        Here's the Rule 90 translation table:

            pattern        111 110 101 100 011 010 001 000
            new state       0   1   0   1   1   0   1   0

        If we assume that a "0" is a safe tile, and a "1" is a trap, then the
        trap conditions in the puzzle description match Rule 90 exactly:

            - Its left and center tiles are traps, but its right tile is not.
              This pattern is "110", which translates as "1".

            - Its center and right tiles are traps, but its left tile is not.
              This pattern is "011", which translates as "1".

            - Only its left tile is a trap. This pattern is "100", which
              translates as "1".

            - Only its right tile is a trap. This pattern is "001", which
              translates as "1".

        All of the trap conditions match "1", and none of them match "0". So,
        for the purposes of this puzzle, we can consider "0" values to be safe
        tiles, and "1" to be traps.
        '''
        # Define the "new_state" table for Rule 90. When we implement our
        # translation, we will look at three digits at a time, and consider
        # them as binary numbers (000 as 0, 001 as 1, 010 as 2, etc.), with the
        # corresponding index in new_state being the new value. Note that the
        # translation table defined in the docstring above (as pulled from the
        # Wikipedia article) is in reverse numerical order, with 111 (i.e. 7)
        # first, and 000 (i.e. 0) last. The Rule 90 translation table happens
        # to be palindromic, so expressing it from 000 to 111 results in the
        # same order as in the table above.
        new_state: tuple[Tile] = (SAFE, TRAP, SAFE, TRAP, TRAP, SAFE, TRAP, SAFE)

        # Width of each line will be the same
        width: int = len(self.first_line)
        # Initialize values for the below loop
        line: str = self.first_line
        safe: int = line.count(SAFE)

        for _ in range(1, num_lines):
            # Columns on either side of the end of each line are considered
            # safe. Surround the line in "safe" tiles to create our pattern.
            pattern: str = f'{SAFE}{line}{SAFE}'
            # Look at 3 characters at a time, and convert to a base 2 integer.
            # This integer's index in the new_state tuple will be the new value
            # generated by Rule 90. We added "safe" tiles to the beginning and
            # end of the previous line to generate our pattern, so peforming
            # this translation $width times on that pattern will result in a
            # new line of the same width as the previous line.
            line = ''.join(
                new_state[int(''.join(pattern[col:col + 3]), 2)]
                for col in range(width)
            )
            # Count the safe tiles and add to the running total
            safe += line.count(SAFE)

        return safe

    def part1(self) -> int:
        '''
        Find and return the shortest path to the destination, given the
        passcode and locking algorithm from the puzzle input.
        '''
        return self.rule90(10 if self.example else 40)

    def part2(self) -> int:
        '''
        Return the length of the longest path to the destination.
        '''
        return self.rule90(400000)


if __name__ == '__main__':
    aoc = AOC2016Day18()
    aoc.run()
