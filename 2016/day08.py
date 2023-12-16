#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/8
'''
import functools
import re
import sys
from collections.abc import Generator

# Local imports
from aoc import AOC

# Typing shortcuts
Coordinate = tuple[int, int]
Operation = tuple[str | None, ...]


class AOC2016Day8(AOC):
    '''
    Day 8 of Advent of Code 2016
    '''
    day = 8
    op_re = re.compile(
        r'rect (\d+)x(\d+)|rotate (row|column) [xy]=(\d+) by (\d+)'
    )

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the object
        '''
        super().__init__(example=example)
        if self.example:
            self.rows = 3
            self.cols = 7
        else:
            self.rows = 6
            self.cols = 50

    @property
    def operations(self) -> Generator[Operation, None, None]:
        '''
        Get one operation at a time from the input file and pass it through the
        regex
        '''
        with self.input.open() as fh:
            for line in fh:
                m = self.op_re.match(line)
                if m:
                    op = [item for item in m.groups() if item is not None]
                    for idx, item in enumerate(op):
                        try:
                            op[idx] = int(op[idx])
                        except ValueError:
                            pass
                    yield tuple(op)

    @functools.cached_property
    def pixels(self) -> set[Coordinate]:
        '''
        Execute all the operations, returning a set containing the coordinates
        of the remaining pixels.
        '''
        pixels = set()
        for op in self.operations:
            match op:
                case (int(col), int(row)):
                    # Turn on each pixel in the specified range
                    pixels.update(
                        (x, y) for x in range(row) for y in range(col)
                    )
                case ('row', int(position), int(delta)):
                    # Extract pixels which are in the target row
                    pixels -= (row := {p for p in pixels if p[0] == position})
                    # Add each pixel in its shifted location
                    pixels.update((x, (y + delta) % self.cols) for x, y in row)
                case ('column', int(position), int(delta)):
                    # Extract pixels which are in the target column
                    pixels -= (col := {p for p in pixels if p[1] == position})
                    # Add each pixel in its shifted location
                    pixels.update(((x + delta) % self.rows, y) for x, y in col)
                case _:
                    raise ValueError(f'Unhandled operation: {op}')

        return pixels

    def print(self, pixels: set[Coordinate]) -> None:
        '''
        Print the contents of the screen to stdout
        '''
        for row in range(self.rows):
            sys.stdout.write(
                ''.join(
                    '*' if (row, col) in pixels else ' '
                    for col in range(self.cols)
                ) + '\n'
            )
        sys.stdout.flush()

    def part1(self) -> int:
        '''
        Return the number of pixels turned on after executing each operation
        '''
        return len(self.pixels)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day8(example=True)
    aoc.validate(aoc.part1(), 6)
    # Run against actual data
    aoc = AOC2016Day8(example=False)
    aoc.run()
    aoc.print(aoc.pixels)
