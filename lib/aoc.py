'''
Base class for Advent of Code submissions
'''
import collections
import sys
import time
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any

# Typing shortcuts
Coordinate = tuple[int, int]

# NOTE: These coordinate deltas are (row, col) instead of (col, row), designed
# for interacting with AoC inputs read in line-by-line.
directions = collections.namedtuple(
    'Directions',
    ('NORTH', 'SOUTH', 'WEST', 'EAST')
)(
    (-1, 0), (1, 0), (0, -1), (0, 1)
)
# This namedtuple is a mirror of above, with the tuple indexes being the
# opposite direction of their counterparts.
opposite_directions = collections.namedtuple(
    'Directions',
    ('SOUTH', 'NORTH', 'EAST', 'WEST')
)(
    (1, 0), (-1, 0), (0, 1), (0, -1)
)

class CoordinateMixin:
    '''
    Functions to do calculations on coordinates
    '''
    @staticmethod
    def distance(p1: Coordinate, p2: Coordinate) -> int:
        '''
        Calculate the number of steps between two coordinates
        '''
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def perimeter(self, bounds: list[Coordinate]) -> int:
        '''
        Calculate the lenth of the perimeter of a polygon, given a list of
        coordinates in either clockwise or counter-clockwise order.
        '''
        return sum(
            self.distance(bounds[n], bounds[n + 1])
            for n in range(len(bounds) - 1)
        )

    @staticmethod
    def shoelace(bounds: list[Coordinate]) -> int:
        '''
        NOTE: bounds must be a list of coordinates in either clockwise or
        counter-clockwise order.

        The area A would be calculated as follows:

            2A = Σ|row(x)*col(x+1) - row(x+1)*col(x)|

        or:

            A = 1/2 * Σ|row(x)*col(x+1) - row(x+1)*col(x)|
        '''
        return abs(
            sum(
                (bounds[n][0] * bounds[n + 1][1]) - (bounds[n + 1][0] * bounds[n][1])
                for n in range(len(bounds) - 1)
            ) // 2
        )


class Grid:
    '''
    Manage a grid as a list of list of strings. Can be indexed like a 2D array.

    Optonally, a callback can be passed when initializing. This callback will
    be run on each column of each line. This can be used to, for example, turn
    each column into an int. For example:

        grid = Grid(path, lambda col: int(col))
    '''
    def __init__(
        self,
        path: Path,
        row_cb: Callable[[str], Any] = lambda col: col,
    ) -> None:
        '''
        Load the file from the Path object
        '''
        self.data = []
        with path.open() as fh:
            self.data = [
                [row_cb(col) for col in line.rstrip()]
                for line in fh
            ]

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
            sys.stdout.write(f'{"".join(str(x) for x in row)}\n')
        sys.stdout.write('\n')
        sys.stdout.flush()

    def column_iter(self) -> Generator[str, None, None]:
        '''
        Generator which yields the contents of the grid one column at a time
        '''
        for col in range(self.cols):
            yield ''.join(
                str(self.data[row][col])
                for row in range(self.rows)
            )


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
