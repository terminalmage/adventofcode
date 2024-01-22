#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/8
'''
import functools
import re
import sys
from collections.abc import Generator

# Local imports
from aoc import AOC, XY

# Typing shortcuts
Operation = tuple[str | int, ...]


class AOC2016Day8(AOC):
    '''
    Day 8 of Advent of Code 2016
    '''
    op_re: re.Pattern = re.compile(
        r'rect (\d+)x(\d+)|rotate (row|column) [xy]=(\d+) by (\d+)'
    )

    def post_init(self) -> None:
        '''
        Set row and column count based on whether or not we are running against
        example data
        '''
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
        for line in self.input.splitlines():
            m: re.Match | None = self.op_re.match(line)
            if m:
                op: list[str] = [item for item in m.groups() if item is not None]
                for idx, item in enumerate(op):
                    try:
                        op[idx] = int(op[idx])
                    except ValueError:
                        pass
                yield tuple(op)

    @functools.cached_property
    def pixels(self) -> set[XY]:
        '''
        Execute all the operations, returning a set containing the coordinates
        of the remaining pixels.
        '''
        # Type hints
        op: Operation

        pixels: set[XY] = set()
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

    def print(self, pixels: set[XY]) -> None:
        '''
        Print the contents of the screen to stdout
        '''
        row: int
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
    # The solution to Part 2 is the printed result, so do that in lieu of a
    # part2 func
    aoc.print(aoc.pixels)
