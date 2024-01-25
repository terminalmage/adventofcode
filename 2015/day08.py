#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/8
'''
# Local imports
from aoc import AOC


class AOC2015Day8(AOC):
    '''
    Day 8 of Advent of Code 2015
    '''
    def part1(self) -> int:
        '''
        Return the difference between the length of the encoded string and the
        length of the printable string
        '''
        return sum(
            len(x) - len(eval(x, {}, {}))  # pylint: disable=eval-used
            for x in self.input.splitlines()
        )

    def part2(self) -> int:
        '''
        Return the difference between the length of the double-encoded strings
        and the original encoded strings. Because we don't need to encode the
        hex chars (we're moving from encoded to double-encoded, not from
        decoded to encoded), the length of each double-encoded string can be
        represented by an algebraic equation:

        x + y = y + z + 2

        where...

        - x is the the difference in size going from encoded to double-encoded

        - y is the length of the original (single-encoded) string

        - z is the number of characters we need to escape. Again, since the
          original string is already encoded, we don't need to consider
          hex-encoding, so the only characters we need to consider are
          backslashes and double-quotes, each of which will need to
          backslash-escaped to double-encode the string.

        - The integer 2 represents the quotes around the new double-encoded
          string

        Solving for x, we get: x = z + 2

        Thus, the difference in size can be represented as the number of
        backslashes and double-quotes, plus 2.
        '''
        return sum(
            x.count('"') + x.count('\\') + 2
            for x in self.input.splitlines()
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day8(example=True)
    aoc.validate(aoc.part1(), 12)
    aoc.validate(aoc.part2(), 19)
    # Run against actual data
    aoc = AOC2015Day8(example=False)
    aoc.run()
