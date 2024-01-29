#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/21
'''
import itertools
import textwrap
from collections.abc import Iterator

# Local imports
from aoc import AOC

# Type hints
Pattern = tuple[tuple[str, ...], ...]


class AOC2017Day21(AOC):
    '''
    Day 21 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        ../.# => ##./#../...
        .#./..#/### => #..#/..../..../#..#
        '''
    )

    validate_part1: int = 12

    def post_init(self) -> None:
        '''
        Load the input patterns. For each pattern, find all possible flipped
        and rotated permutations, and construct a dictionary mapping the
        possible subgrid arrangements to the expanded output.
        '''
        self.start: Pattern = ('.#.', '..#', '###')

        self.rules: dict[Pattern, Pattern] = {}

        for line in self.input.splitlines():
            in_grid: tuple[str]
            out_grid: tuple[str]
            in_grid, out_grid = (
                tuple(item.split('/')) for item in line.split(' => ')
            )

            # All rotations of the input pattern
            matches: Iterator[Pattern] = self.matches(in_grid)
            # The output subgrid
            output: Iterator[Pattern] = itertools.repeat(out_grid)

            # Add a mapping to our rules dict for each flipped and rotated
            # permitation of the input pattern, mapping each of them to the
            # output pattern.
            self.rules.update(zip(matches, output))

    def matches(self, pat: Pattern) -> Iterator[Pattern]:
        '''
        Rotate and flip the pattern 4 times, yielding all results
        '''
        for _ in range(4):
            yield (
                pat := tuple(
                    ''.join(pat[i][j] for i in range(len(pat)))
                    for j in range(len(pat[0]) - 1, -1, -1)
                )
            )
            yield tuple(''.join(reversed(line)) for line in pat)

    def enhance(self, rounds: int) -> Pattern:
        '''
        Assuming a 4x4 grid, we would divide it into 4 2x2 subgrids, processed
        in alphabetical order:

            AC
            BD

        We will process these in the order A, C, B, D. First, subgrid A will be
        expanded into a 3-line subgrid. We would then expand C, resulting in
        another 3 lines being added to our result. Once we finish all subgrids
        in the first column, we continue to subgrid B. For each line in the
        expanded version of subgrid B, we append the result to the lines from
        A. Finally, we expand D, appending each lines to the lines we
        originally added when we expanded C. At the end of these expansions and
        appends, we will have a new 6x6 grid.

        To enhance a 6x6 grid, we would divide it into 9 2x2 subgrids, because
        6 divisible by 2. It is also divisible by 3, but even sizes that are
        divisible by 3 are subdivided into 2x2 grids instead of 3x3 grids. The
        9 subgrids would be processed in alphabetical order as laid out below:

            ADG
            BEH
            CFI

        Repeat this process for the specified number of rounds
        '''
        grid: Pattern = self.start

        for _ in range(rounds):

            size: int = 2 if len(grid) % 2 == 0 else 3
            subgrid_size: int = len(grid) // size
            new_grid: list[str] = []

            for col in range(subgrid_size):
                for row in range(subgrid_size):
                    row_start: int = size * row
                    col_start: int = size * col
                    # Extract the subgrid from the grid passed in
                    subgrid: Pattern = tuple(
                        grid[row][col_start:col_start + size]
                        for row in range(row_start, row_start + size)
                    )
                    expanded: Pattern = self.rules[subgrid]
                    # Append expanded subgrid to the new grid
                    for line_num, line in enumerate(expanded):
                        index: int = (row * len(expanded)) + line_num
                        try:
                            new_grid[index] += line
                        except IndexError:
                            new_grid.append(line)

            grid = tuple(new_grid)

        return grid

    @staticmethod
    def count_pixels(grid: Pattern) -> int:
        '''
        Return the number of pixels in the grid that are "on"
        '''
        return ''.join(grid).count('#')

    def part1(self) -> int:
        '''
        Return the number of pixels turned on after 5 rounds
        '''
        rounds: int = 2 if self.example else 5
        return self.count_pixels(self.enhance(rounds=rounds))

    def part2(self) -> int:
        '''
        Return the number of pixels turned on after 18 rounds
        '''
        return self.count_pixels(self.enhance(rounds=18))


if __name__ == '__main__':
    aoc = AOC2017Day21()
    aoc.run()
