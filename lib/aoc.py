'''
Base class for Advent of Code submissions
'''
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

class Grid:
    '''
    Handle initializing a grid as a 2-dimensional array
    '''
    def __init__(self, path: Path) -> None:
        '''
        Load the filehandle
        '''
        self.data = []
        with path.open() as fh:
            for line in fh:
                self.data.append([])
                self.data[-1].extend(line.rstrip())

    def __getitem__(self, index: int) -> list[str]:
        '''
        Allow object to be indexed like a list
        '''
        return self.data[index]

    @property
    def rows(self) -> int:
        '''
        Return the number of rows in the grid
        '''
        return len(self.data)

    @property
    def cols(self) -> int:
        '''
        Return the number of columns in the grid
        '''
        return len(self.data[0])

    def print(self) -> None:
        '''
        Print the grid to stdout
        '''
        for row in self.data:
            sys.stdout.write(f'{"".join(row)}\n')
        sys.stdout.write('\n')
        sys.stdout.flush()


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
