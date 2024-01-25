#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/8
'''
from __future__ import annotations
import textwrap

# Local imports
from aoc import AOC


class AOC2022Day8(AOC):
    '''
    Day 8 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        30373
        25512
        65332
        33549
        35390
        '''
    )

    validate_part1: int = 21
    validate_part2: int = 8

    def post_init(self) -> None:
        '''
        Load the datastream
        '''
        self.trees: list[list[int]] = [
            [int(item) for item in line]
            for line in self.input.splitlines()
        ]

        self.last_row: int = len(self.trees) - 1
        self.last_col: int = len(self.trees[0]) - 1

    def visible(
        self,
        x: int,
        y: int,
    ) -> bool:
        '''
        Check whether a tree at the given coordinates is visible
        '''
        # Any tree on the perimiter is visible
        if x in (0, self.last_col) or y in (0, self.last_row):
            return True

        try:
            height: int = self.trees[y][x]
        except IndexError as exc:
            raise ValueError(f'Coordinate ({x},{y}) is out of bounds') from exc

        if all(   # Check from north -> south
            item < height for item in (
                self.trees[row][x] for row in range(0, y)
            )
        ) or all( # Check from south -> north
            item < height for item in (
                self.trees[row][x] for row in range(self.last_row, y, -1)
            )
        ) or all( # Check from west -> east
            item < height for item in (
                self.trees[y][col] for col in range(0, x)
            )
        ) or all( # Check from east -> west
            item < height for item in (
                self.trees[y][col] for col in range(self.last_col, x, -1)
            )
        ):
            return True

        return False

    def scenic_score(
        self,
        x: int,
        y: int,
    ) -> int:
        '''
        Return the scenic score of a tree at the given coordinates
        '''
        try:
            height: int = self.trees[y][x]
        except IndexError as exc:
            raise ValueError(f'Coordinate ({x},{y}) is out of bounds') from exc

        north: int
        south: int
        east: int
        west: int
        item: int

        north = south = east = west = 0

        # Check to the north
        for item in (self.trees[row][x] for row in range(y - 1, -1, -1)):
            north += 1
            if item >= height:
                break

        # Check to the south
        for item in (self.trees[row][x] for row in range(y + 1, self.last_row + 1)):
            south += 1
            if item >= height:
                break

        # Check to the west
        for item in (self.trees[y][col] for col in range(x - 1, -1, -1)):
            west += 1
            if item >= height:
                break

        # Check to the south
        for item in (self.trees[y][col] for col in range(x + 1, self.last_col + 1)):
            east += 1
            if item >= height:
                break

        return north * south * east * west

    def part1(self) -> int:
        '''
        Calculate the number of visible trees
        '''
        return sum(
            1 for (col, row) in (
                (x, y) for x in range(self.last_col + 1)
                for y in range(self.last_row + 1)
            )
            if self.visible(col, row)
        )

    def part2(self) -> int:
        '''
        Calculate the max Scenic Score™
        '''
        return max(
            self.scenic_score(x, y)
            for x in range(self.last_col + 1)
            for y in range(self.last_row + 1)
        )


if __name__ == '__main__':
    aoc = AOC2022Day8()
    aoc.run()
