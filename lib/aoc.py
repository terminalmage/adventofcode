'''
Base class for Advent of Code submissions
'''
import sys
from pathlib import Path
from typing import Any


class AOC:
    '''
    Base class for Advent of Code submissions
    '''
    # Must be overridden in a subclass
    day = 0

    def __init__(self, example: bool = False) -> None:
        '''
        Create Path object for the input file
        '''
        self.example = example
        prefix = 'example' if self.example else 'day'
        self.input = Path(__file__).parent.joinpath(
            'inputs',
            f'{prefix}{str(self.day).zfill(2)}.txt',
        )

    def get_input(self, part: int) -> Path:
        '''
        Disambiguation function that accounts for cases where the example data
        for part two is different from part one
        '''
        if not self.example:
            return self.input

        return Path(__file__).parent.joinpath(
            'inputs',
            f'example{str(self.day).zfill(2)}part{part}.txt',
        )

    @staticmethod
    def validate(lvalue: Any, rvalue: Any) -> None:
        '''
        Perform an assertion error and print a meaningful error on failure
        '''
        try:
            assert lvalue == rvalue
        except AssertionError:
            sys.stderr.write(
                f'Validation failed! Expected {rvalue}, got {lvalue}\n'
            )
            sys.exit(1)

    def run(self):
        '''
        Run both parts and print the results
        '''
        header = f'Result for Day {self.day}'
        print(header)
        print('-' * len(header))
        print(f'Answer 1: {self.part1()}')  # pylint: disable=no-member
        if hasattr(self, 'part2'):
            print(f'Answer 2: {self.part2()}')
