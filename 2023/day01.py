#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/1
'''
import re

# Local imports
from aoc import AOC


class AOC2023Day1(AOC):
    '''
    Day 1 of Advent of Code 2023
    '''
    day = 1

    digits = re.compile(r'\d')
    digit_words = re.compile(
        r'(?=(\d|(?:zero|one|two|three|four|five|six|seven|eight|nine)))'
    )

    def part1(self) -> int:
        '''
        Return the sum of all the calibration values
        '''
        values = []
        with self.get_input(part=1).open() as fh:
            for line in fh:
                digits = self.digits.findall(line)
                values.append(int(f'{digits[0]}{digits[-1]}'))

        return sum(values)

    def part2(self) -> int:
        '''
        Return the sum of all the calibration values
        '''
        digit_map = {
            'zero': 0,
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
        }

        def resolve(digit: str) -> int:
            '''
            Given a string representation of a digit (either a full word, or a
            string integer), return the integer value.
            '''
            try:
                return int(digit)
            except (TypeError, ValueError):
                try:
                    return digit_map[digit]
                except KeyError as exc:
                    raise ValueError(f'Invalid digit: {digit!r}') from exc

        values = []
        with self.get_input(part=2).open() as fh:
            for line in fh:
                digits = self.digit_words.findall(line)
                values.append(int(f'{resolve(digits[0])}{resolve(digits[-1])}'))

        return sum(values)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day1(example=True)
    aoc.validate(aoc.part1(), 142)
    aoc.validate(aoc.part2(), 281)
    # Run against actual data
    aoc = AOC2023Day1(example=False)
    aoc.run()
