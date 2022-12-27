#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/8

--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted
carefully in a grid. The Elves explain that a previous expedition planted these
trees as a reforestation effort. Now, they're curious if this would be a good
location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house
hidden. To do this, you need to count the number of trees that are visible from
outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height
of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0
is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid
are shorter than it. Only consider trees in the same row or column; that is,
only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are
already on the edge, there are no trees to block the view. In this example,
that only leaves the interior nine trees to consider:

- The top-left 5 is visible from the left and top. (It isn't visible from the
  right or bottom since other trees of height 5 are in the way.)

- The top-middle 5 is visible from the top and right.

- The top-right 1 is not visible from any direction; for it to be visible,
  there would need to only be trees of height 0 between it and an edge.

- The left-middle 5 is visible, but only from the right.

- The center 3 is not visible from any direction; for it to be visible, there
  would need to be only trees of at most height 2 between it and an edge.

- The right-middle 3 is visible from the right.

- In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a
total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

'''
from __future__ import annotations

# Local imports
from aoc import AOC


class AOC2022Day8(AOC):
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

    def part1(self) -> int:
        '''
        Calculate the number of visible trees
        '''
        return sum(
            1 for (col, row) in (
                (x, y) for x in range(aoc.last_col + 1)
                for y in range(aoc.last_row + 1)
            )
            if aoc.visible(col, row)
        )

    def part2(self) -> int:
        '''
        Calculate the max Scenic Score™
        '''
        return max(
            aoc.scenic_score(x, y)
            for x in range(aoc.last_col + 1)
            for y in range(aoc.last_row + 1)
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day8(example=True)
    aoc.validate(aoc.part1(), 21)
    aoc.validate(aoc.part2(), 8)
    # Run against actual data
    aoc = AOC2022Day8(example=False)
    aoc.run()
