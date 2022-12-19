'''
Commom Functions
'''
import sys
from pathlib import Path
from typing import Any


class AOC2022:
    '''
    Base class for Advent of Code 2022
    '''
    # Override this for each day
    day = 0

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the object
        '''
        self.example = example
        prefix = 'example' if self.example else 'day'
        self.input = Path(__file__).parent.parent.joinpath(
            'inputs',
            f'{prefix}{str(self.day).zfill(2)}.txt',
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
        print(f'Answer 1: {self.part1()}')
        print(f'Answer 2: {self.part2()}')
