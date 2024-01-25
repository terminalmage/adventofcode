#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/1
'''
import re
import textwrap

# Local imports
from aoc import AOC


class AOC2023Day1(AOC):
    '''
    Day 1 of Advent of Code 2023
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
        '''
    )
    example_data_part2: str = textwrap.dedent(
        '''
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
        '''
    )

    validate_part1: int = 142
    validate_part2: int = 281

    digits: re.Pattern = re.compile(r'\d')
    digit_words: re.Pattern = re.compile(
        r'(?=(\d|(?:zero|one|two|three|four|five|six|seven|eight|nine)))'
    )

    def part1(self) -> int:
        '''
        Return the sum of all the calibration values
        '''
        values: list[int] = []
        line: str
        for line in self.input_part1.splitlines():
            digits: list[str] = self.digits.findall(line)
            values.append(int(f'{digits[0]}{digits[-1]}'))

        return sum(values)

    def part2(self) -> int:
        '''
        Return the sum of all the calibration values
        '''
        digit_map: dict[str, int] = {
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

        values: list[int] = []
        for line in self.input_part2.splitlines():
            digits: list[str] = self.digit_words.findall(line)
            values.append(int(f'{resolve(digits[0])}{resolve(digits[-1])}'))

        return sum(values)


if __name__ == '__main__':
    aoc = AOC2023Day1()
    aoc.run()
