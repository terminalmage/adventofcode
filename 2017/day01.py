#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/1
'''
import re

# Local imports
from aoc import AOC


class AOC2017Day1(AOC):
    '''
    Day 1 of Advent of Code 2017
    '''
    day = 1

    def part1(self) -> int:
        '''
        Return the CAPTCHA solution for Part 1
        '''
        # To ensure that the final char of the string is compared to the
        # beginning of the string, add the first char in the string to the end.
        captcha = self.get_input(part=1).read_text().strip()
        captcha += captcha[0]
        return sum(int(dup) for dup in re.findall(r'(\d)(?=\1)', captcha))

    def part2(self) -> int:
        '''
        Return the CAPTCHA solution for Part 2
        '''
        # To ensure that, no matter where in the captcha we are, we can use a
        # lookahead to reach halfway around the captcha text, append the first
        # half of the captcha to the end.
        captcha = self.get_input(part=2).read_text().strip()
        half: int = len(captcha) // 2
        captcha += captcha[:half]

        # We want to programatically arrive at the following regex:
        #
        #   (\d)(?=.{n}\1)
        #
        # Where "n" is half the length of the captcha minus 1. This regex
        # captures a single digit, then performs a lookahead. This lookahead
        # essentially ignores half-1 digits, and then matches if and only if
        # the following character is the same as the first digit matched.
        #
        # The result is the f-string you see below. The f-string interpolation
        # process first encounters the 2 consecutive open curly braces "{{" and
        # interprets them as a literal open curly brace "{". It next encounters
        # {half-1} and replaces it with the value of the variable "half"
        # (defined above) minus 1. Finally, it encounters the two consecutive
        # close curly braces "}}" and interprets them as a literal close curly
        # brace "}".
        return sum(
            int(dup) for dup in re.findall(
                rf'(\d)(?=.{{{half-1}}}\1)',
                captcha,
            )
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2017Day1(example=True)
    aoc.validate(aoc.part1(), 9)
    aoc.validate(aoc.part2(), 4)
    # Run against actual data
    aoc = AOC2017Day1(example=False)
    aoc.run()
