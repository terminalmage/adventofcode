#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/5
'''
import re
import textwrap

# Local imports
from aoc import AOC


class AOC2015Day5(AOC):
    '''
    Day 5 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        ugknbfddgicrmopn
        aaa
        jchzalrnumimnmhp
        haegwjzuvuyypxyu
        dvszwmarrgswjxmb
        '''
    )

    validate_part1: int = 2
    validate_part2: int = 2

    # Set by post_init
    strings = None

    def post_init(self) -> None:
        '''
        Load the strings
        '''
        self.strings: list[str] = self.input.splitlines()

    def part1(self) -> int:
        '''
        Return the number of strings which are nice under Part 1's rules
        '''
        vowels_re: re.Pattern = re.compile(r'[aeiou]')
        duplicate_re: re.Pattern = re.compile(r'([a-z])\1')
        verboten_re: re.Pattern = re.compile('ab|cd|pq|xy')
        return sum(
            1 for item in self.strings
            if len(vowels_re.findall(item)) > 2
                and bool(duplicate_re.search(item))
                and not bool(verboten_re.search(item))
        )

    def part2(self) -> int:
        '''
        Return the number of strings which are nice under Part 2's rules
        '''
        strings: tuple[str, ...] = (
            'qjhvhtzxzqqjkmpb',
            'xxyxx',
            'uurcxstgmygtbstg',
            'ieodomkazucvgmuy',
        ) if self.example else self.strings

        repeat_re: re.Pattern = re.compile(r'([a-z]{2}).*\1')
        sandwich_re: re.Pattern = re.compile(r'([a-z])[a-z]\1')
        return sum(
            1 for item in strings
            if bool(repeat_re.search(item)) and bool(sandwich_re.search(item))
        )


if __name__ == '__main__':
    aoc = AOC2015Day5()
    aoc.run()
