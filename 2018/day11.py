#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/11
'''
import textwrap

# Local imports
from aoc import AOC

Row = tuple[int, ...]
FuelGrid = tuple[Row, ...]


class AOC2018Day11(AOC):
    '''
    Day 11 of Advent of Code 2018
    '''
    grid_size: int = 300

    example_data: str = textwrap.dedent(
        '''
        18
        '''
    )

    validate_part1: tuple[int, int] = '33,45'
    validate_part2: tuple[int, int] = '90,269,16'

    # Set by post_init
    serial = None
    grid = None

    def post_init(self) -> None:
        '''
        Load the numbers from the example data, and create a summed-area table
        '''
        self.serial: int = int(self.input)

        # Initialize the grid with all zeroes. Note that the dimensions will
        # actually be 301x301. Since calculation of the summed-area table
        # references coordinates x-1 and y-1, the top row and leftmost column
        # will remain all zeroes so that we don't have to worry about
        # handling an IndexError.
        grid: list[list[int]] = [
            [0 for _ in range(self.grid_size + 1)]
            for _ in range(self.grid_size + 1)
        ]

        # Calculate the power level using the algorithm described in the puzzle
        x: int
        y: int
        for x in range(1, self.grid_size + 1):
            for y in range(1, self.grid_size + 1):
                rack_id: int = x + 10
                grid[x][y] = (
                    ((((rack_id * y) + self.serial) * rack_id) // 100) % 10
                ) - 5

        # Replace grid values with summed area values in a single pass
        # See: https://en.wikipedia.org/wiki/Summed-area_table#The_algorithm
        for x in range(1, self.grid_size + 1):
            for y in range(1, self.grid_size + 1):
                grid[x][y] = (
                    grid[x][y]
                    + grid[x][y - 1]
                    + grid[x - 1][y]
                    - grid[x - 1][y - 1]
                )

        # Freeze the table into an immutable tuple of tuples
        self.grid: FuelGrid = tuple(tuple(row) for row in grid)

    def solve(self, side_length: int) -> tuple[int, tuple[int, int, int]]:
        '''
        Calculate the largest power level for a square with the sides of the
        specified length.

        This function returns a tuple containing the following:

            1. An integer containing the highest power level
            2. A triple containing the XY coordinate followed by the number of
               fuel cells in the grid (i.e. the side_length, squared)

        Use the summed-area table (computed in the post_init function) to
        compute power levels. See the following link for details:

        https://en.wikipedia.org/wiki/Summed-area_table#The_algorithm

        The sum of an arbitrary rectangular block of values from the original
        data can be calculated using values from the summed-area table.
        Specifically, use the corresponding bottom-right coordinate (D), and
        then the X,Y coordinates one above and to the left (A, B, and C).

         A                      B
          +--------------------+
          |+-------------------+
          ||                   |
          ||                   |
          ++-------------------+
         C                      D

        The result is equal to D - B - C + A.

        '''
        best: tuple[int, tuple[int, int]] = (0, (0, 0, side_length))

        for x in range(self.grid_size - side_length + 1):
            for y in range(self.grid_size - side_length + 1):
                A: int = self.grid[x][y]
                B: int = self.grid[x + side_length][y]
                C: int = self.grid[x][y + side_length]
                D: int = self.grid[x + side_length][y + side_length]
                # The coordinate (x, y) is equivalent to point A in the diagram
                # above. Thus, the top-left coordinate of the square is
                # actually located at (x + 1, y + 1).
                best = max(best, (D - B - C + A, (x + 1, y + 1, side_length)))

        return best

    @staticmethod
    def format(result: tuple[int, ...]) -> str:
        '''
        Given a tuple of integers, return as a comma-separated string
        '''
        return ','.join(str(i) for i in result)

    def part1(self) -> str:
        '''
        Return the top-left coordinate of the 3x3 square of fuel cells with the
        highest combined power level.
        '''
        return self.format(self.solve(side_length=3)[1][:2])

    def part2(self) -> str:
        '''
        Return the top-left coordinate of the largest square of _any_ size
        with the highest combined power level.
        '''
        best: tuple[int, tuple[int, int]] = (0, (0, 0, 0))
        side_length: int
        for side_length in range(1, self.grid_size):
            best = max(best, self.solve(side_length=side_length))

        return self.format(best[1])


if __name__ == '__main__':
    aoc = AOC2018Day11()
    aoc.run()
