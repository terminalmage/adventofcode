#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/11
'''
import itertools
import re
import textwrap

# Local imports
from aoc import AOC, XY

# Typing shortcuts
Galaxy = XY
Universe = list[Galaxy]


class AOC2023Day11(AOC):
    '''
    Day 11 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        '''
    )

    validate_part1: int = 374
    validate_part2: int = 8410

    # Set by post_init
    universe = None

    def post_init(self) -> None:
        '''
        Make an apple pie from scratch
        '''
        self.universe: list[Galaxy] = []
        for row_num, row in enumerate(self.input.splitlines()):
            self.universe.extend(
                (row_num, m.start())
                for m in re.finditer(r'#', row)
            )

    @staticmethod
    def expand(
        universe: Universe,
        factor: int = 2,
    ) -> Universe:
        '''
        Expand a universe by adding extra rows/cols in place of empty ones,
        returning a new Universe.
        '''
        if factor < 2:
            raise ValueError('factor must be >= 2')

        # Get all the empty rows and cols
        rows: set[int]
        cols: set[int]
        rows, cols = (set(x) for x in zip(*universe))
        empty_rows: list[int] = [x for x in range(max(rows)) if x not in rows]
        empty_cols: list[int] = [x for x in range(max(cols)) if x not in cols]

        expanded: Galaxy = []
        row_trans: dict[int, int] = {}
        col_trans: dict[int, int] = {}

        row: int
        col: int
        for (row, col) in universe:
            if row in row_trans:
                # Use already-calculated translated row number, if one exists
                row = row_trans[row]
            elif row < empty_rows[0]:
                # If the row number is less than the lowest row number, then no
                # translation needs to be done. Save the value for future
                # iterations.
                row_trans[row] = row
            else:
                # Enumerating the list of empty rows produces a sequence of
                # multiplier indexes and row numbers where there are gaps. By
                # reversing this sequence of tuples, we can check if the
                # current galaxy's row number comes after a given empty row. If
                # so, then the translated row number can be calculated by
                # multiplying the index by the number of rows we need to add
                # (i.e. the growth factor minus 1).
                index: int
                gap: int
                for index, gap in reversed(list(enumerate(empty_rows, 1))):
                    if row > gap:
                        # Calculate number of rows to add
                        delta = index * (factor - 1)
                        row_trans[row] = row + delta
                        row += delta
                        break

            # Perform all the same translation logic as above, only on the
            # columns. I'm sure there's a more elegant way of doing this.
            if col in col_trans:
                col = col_trans[col]
            elif col < empty_cols[0]:
                col_trans[col] = col
            else:
                for index, gap in reversed(list(enumerate(empty_cols, 1))):
                    if col > gap:
                        delta = index * (factor - 1)
                        col_trans[col] = col + delta
                        col += delta
                        break

            expanded.append((row, col))

        return expanded

    @staticmethod
    def distance(g1: Galaxy, g2: Galaxy) -> int:
        '''
        Calculate the number of steps between two galaxies
        '''
        return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])

    def solve(self, factor: int = 2):
        '''
        Return the sum of the shortest distance between each galaxy and each of
        its neighbors.
        '''
        return sum(
            self.distance(g1, g2)
            for g1, g2 in itertools.combinations(
                self.expand(self.universe, factor=factor), 2
            )
        )

    def part1(self) -> int:
        '''
        Solve for Part 1, with a growth factor of 2
        '''
        return self.solve()

    def part2(self) -> int:
        '''
        Solve for Part 2, with a growth factor of 1000000
        '''
        factor = 100 if self.example else 1000000
        return self.solve(factor=factor)


if __name__ == '__main__':
    aoc = AOC2023Day11()
    aoc.run()
