'''
Base class for Advent of Code submissions
'''
import sys
import time
from collections.abc import Callable
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

    @staticmethod
    def timed_exec(
        label: str,
        func: Callable[[], Any],
    ) -> None:
        '''
        Time the function
        '''
        start = time.time()
        ret = func()
        total = time.time() - start
        print(f'{label}: {ret} ({total} seconds)')  # pylint: disable=no-member

    def run(self):
        '''
        Run both parts and print the results
        '''
        header = f'Result for Day {self.day}'
        print(header)
        print('-' * len(header))
        for part in (1, 2):
            if hasattr(self, f'part{part}'):
                self.timed_exec(f'Answer {part}', getattr(self, f'part{part}'))
