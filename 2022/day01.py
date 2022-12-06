#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/1
'''
# Local imports
from aoc2022 import AOC2022


WINS = {
    'rock': 'paper',
    'paper': 'scissors',
    'scissors': 'rock',
}
LOSES = {val: key for key, val in WINS.items()}


class AOC2022Day1(AOC2022):
    '''
    Day 1 of Advent of Code 2022
    '''
    day = 1

    def __init__(self) -> None:
        '''
        Calculate calories
        '''
        super().__init__()
        self.elf_calories = {}
        with self.input.open() as fh:
            elf_number = 1
            calories = 0
            for line in fh:
                try:
                    calories += int(line.rstrip('\n'))
                except ValueError:
                    # We've reached the blank line dividing groups of snacks.
                    # Save the result, and then zero out the calorie count and
                    # increment the elf number
                    self.elf_calories[elf_number] = calories
                    calories = 0
                    elf_number += 1

            # When we get to the end of the file the exception above won't
            # trigger, so we need to save the last elf's calories.
            self.elf_calories[elf_number] = calories


if __name__ == '__main__':
    aoc = AOC2022Day1()
    answer1 = max(aoc.elf_calories.values())
    print(f'Answer 1 (top calorie count): {answer1}')
    answer2 = sum(sorted(aoc.elf_calories.values(), reverse=True)[:3])
    print(f'Answer 2 (sum of top 3 calorie counts): {answer2}')
