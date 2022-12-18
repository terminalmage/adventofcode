#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/8
'''
from __future__ import annotations

# Local imports
from aoc2022 import AOC2022


class AOC2022Day8(AOC2022):
    '''
    Day 8 of Advent of Code 2022
    '''
    day = 8

    def __init__(self, example: bool = False) -> None:
        '''
        Load the datastream
        '''
        super().__init__(example=example)

        self.trees = []

        with self.input.open() as fh:
            for line in fh:
                self.trees.append([int(item) for item in line.rstrip('\n')])

        self.last_row = len(self.trees) - 1
        self.last_col = len(self.trees[0]) - 1

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
            height = self.trees[y][x]
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
            height = self.trees[y][x]
        except IndexError as exc:
            raise ValueError(f'Coordinate ({x},{y}) is out of bounds') from exc

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


if __name__ == '__main__':
    aoc = AOC2022Day8()
    answer1 = sum(
        1 for (col, row) in (
            (x, y) for x in range(aoc.last_col + 1)
            for y in range(aoc.last_row + 1)
        )
        if aoc.visible(col, row)
    )
    print(f'Answer 1 (number of visible trees): {answer1}')
    answer2 = max(
        aoc.scenic_score(x, y)
        for x in range(aoc.last_col + 1)
        for y in range(aoc.last_row + 1)
    )
    print(f'Answer 1 (max scenic score): {answer2}')
