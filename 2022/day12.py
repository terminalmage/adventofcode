#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/12

--- Day 12: Hill Climbing Algorithm ---

You try contacting the Elves using your handheld device, but the river you're
following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input).
The heightmap shows the local area from above broken into a grid; the elevation
of each square of the grid is given by a single lowercase letter, where a is
the lowest elevation, b is the next-lowest, and so on up to the highest
elevation, z.

Also included on the heightmap are marks for your current position (S) and the
location that should get the best signal (E). Your current position (S) has
elevation "a", and the location that should get the best signal (E) has
elevation "z".

You'd like to reach E, but to save energy, you should do it in as few steps as
possible. During each step, you can move exactly one square up, down, left, or
right. To avoid needing to get out your climbing gear, the elevation of the
destination square can be at most one higher than the elevation of your current
square; that is, if your current elevation is "m", you could step to elevation
"n", but not to elevation "o". (This also means that the elevation of the
destination square can be much lower than the elevation of your current
square.)

For example:

    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi

Here, you start in the top-left corner; your goal is near the middle. You could
start by moving down or right, but eventually you'll need to head toward the
"e" at the bottom. From there, you can spiral around to the goal:

    v..v<<<<
    >v.vv<<^
    .>vv>E^^
    ..v>>>^^
    ..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square
moving up (^), down (v), left (<), or right (>). The location that should get
the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the
location that should get the best signal?

--- Part Two ---

As you walk up the hill, you suspect that the Elves will want to turn this into
a hiking trail. The beginning isn't very scenic, though; perhaps you can find a
better starting point.

To maximize exercise while hiking, the trail should start as low as possible:
elevation a. The goal is still the square marked E. However, the trail should
still be direct, taking the fewest steps to reach its goal. So, you'll need to
find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi

Now, there are six choices for starting position (five marked a, plus the
square marked S that counts as being at elevation a). If you start at the
bottom-left square, you can reach the goal most quickly:

    ...v<<<<
    ...vv<<^
    ...v>E^^
    .>v>>>^^
    >^>>>>>^

This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with
elevation a to the location that should get the best signal?
'''
from __future__ import annotations
import collections
import re

# Local imports
from aoc2022 import AOC2022

# Typing shortcuts
Coordinate = tuple[int, int]


class AOC2022Day12(AOC2022):
    '''
    Base class for Day 12 of Advent of Code 2022
    '''
    day = 12

    def __init__(self, example: bool = False) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        super().__init__(example=example)

        self.nodes = []
        valid = re.compile('^[a-zSE]+$')
        self.start = None
        self.end = None

        for row, line in enumerate(self.input.read_text().splitlines()):
            if not valid.match(line):
                raise ValueError(
                    f'Line #{row + 1} contains one or more invalid characters'
                )
            self.nodes.append([])
            for col, value in enumerate(line):
                coord = (row, col)
                if value == 'E':
                    if self.end is not None:
                        raise ValueError('More than one end point found')
                    self.end = coord
                    value = 'z'
                elif value == 'S':
                    if self.start is not None:
                        print(self.start)
                        raise ValueError('More than one start point found')
                    self.start = coord
                    value = 'a'

                # Assign an integer elevation for this coordinate. Lowercase
                # a-z letters have contiguous ordinal values, so ord(x) works
                # well as an elevation value.
                self.nodes[row].append(ord(value))

        self.num_rows = len(self.nodes)
        self.num_cols = len(self.nodes[0])

    def neighbors(self, row: int, col: int) -> Iterator[Coordinate]:
        '''
        Return all neighbors of the specified coordinate
        '''
        for neighbor_row, neighbor_col in (
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1),
        ):
            if (
                0 <= neighbor_row < self.num_rows and
                0 <= neighbor_col < self.num_cols
            ):
                # Make sure to only yield coordinates that are in bounds
                yield neighbor_row, neighbor_col

    def matches(self, char: int) -> Iterator[Coordinate]:
        '''
        Generator which returns all coordinates matching the specified
        character
        '''
        elevation = ord(char)
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.nodes[row][col] == elevation:
                    yield row, col

    def bfs(self, *starting_points: Sequence[Coordinate]) -> int:
        '''
        Use breadth-first search to find distance of shortest path
        '''
        if not starting_points:
            raise ValueError(f'At least one start point is required')

        visited = set()

        dq = collections.deque((start, 0) for start in starting_points)

        while dq:
            coord, distance = dq.popleft()
            if coord == self.end:
                return distance

            elevation = self.nodes[coord[0]][coord[1]]
            for neighbor_coord in self.neighbors(*coord):
                row, col = neighbor_coord
                if (
                    1 >= (self.nodes[row][col] - elevation)
                    and neighbor_coord not in visited
                ):
                    visited.add(neighbor_coord)
                    dq.append((neighbor_coord, distance + 1))


if __name__ == '__main__':
    aoc = AOC2022Day12()
    print(f'Answer 1 (minimum number of steps from start): {aoc.bfs(aoc.start)}')
    elev = 'a'
    print(
        f'Answer 2 (minimum number of steps from elevation {elev!r}): '
        f'{aoc.bfs(*aoc.matches(elev))}'
    )
