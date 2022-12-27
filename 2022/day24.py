#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/24
'''
import collections
import functools

# Local imports
from aoc import AOC

# Right, down, wait, left, up
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STAY_PUT = (0, 0)
MOVES = (UP, DOWN, LEFT, RIGHT, STAY_PUT)

# Typing shortcuts
Coordinate = tuple[int, int]


class AOC2022Day24(AOC):
    '''
    Day 24 of Advent of Code 2022
    '''
    day = 24

    def __init__(self, example: bool = False) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        super().__init__(example=example)
        with self.input.open() as fh:
            lines = fh.read().splitlines()[1:-1]

        blizzard_map = {'^': 'up', 'v': 'down', '<': 'left', '>': 'right'}
        blizzards = {direction: set() for direction in blizzard_map.values()}

        for row, line in enumerate(lines):
            for col, item in enumerate(line[1:-1]):
                if item in blizzard_map:
                    blizzards[blizzard_map[item]].add((col, row))

        for direction, coords in blizzards.items():
            setattr(self, f'{direction}_blizzards', frozenset(coords))

        self.height = len(lines)
        self.width = len(lines[0]) - 2

        self.entrance = (0, 0)
        self.exit = (self.width - 1, self.height - 1)

    def can_move(
        self,
        position: Coordinate,
        timestamp: int,
    ) -> bool:
        '''
        Since blizzards wrap around in each direction, their positions can be
        represented as their original position plus the timestamp, modulo the
        height/width of the grid
        '''
        col, row = position
        # pylint: disable=no-member
        return not any((
            (col, (row + timestamp) % self.height) in self.up_blizzards,
            (col, (row - timestamp) % self.height) in self.down_blizzards,
            ((col + timestamp) % self.width, row) in self.left_blizzards,
            ((col - timestamp) % self.width, row) in self.right_blizzards,
        ))
        # pylint: enable=no-member

    def bfs(
        self,
        start: Coordinate | None = None,
        end: Coordinate | None = None,
        init_timestamp: int = 0,
    ) -> int:
        '''
        Use breadth-first search to find time spent in shortest path
        '''
        start = start or self.entrance
        end = end or self.exit

        visited = set()

        dq = collections.deque()

        while True:
            while not dq:
                # Ensure we count the first minute(s), in which we can either
                # A) enter the valley, or B) wait for blizzard(s) to pass
                init_timestamp += 1
                # Check to see if the coast is clear
                if self.can_move(start, init_timestamp):
                    dq.append((start, init_timestamp))

            coord, timestamp = dq.popleft()

            if (coord, timestamp) in visited:
                continue

            visited.add((coord, timestamp))
            if coord == end:
                return timestamp + 1  # Add a second to factor in the final step

            for delta in MOVES:
                # Only consider moves that are within the bounds, and which are
                # not blocked by a blizzard
                new_pos = tuple(sum(x) for x in zip(coord, delta))
                if (
                    0 <= new_pos[0] < self.width and
                    0 <= new_pos[1] < self.height and
                    self.can_move(new_pos, timestamp + 1)
                ):
                    dq.append((new_pos, timestamp + 1))

    @functools.lru_cache
    def part1(self) -> int:
        '''
        Calculate the quickest you can get from the start to the end
        '''
        return self.bfs()

    def part2(self) -> int:
        '''
        Calculate the quickest you can get from start to end and back again
        '''
        return self.bfs(
            init_timestamp=self.bfs(
                start=self.exit,
                end=self.entrance,
                init_timestamp=self.part1(),
            ),
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day24(example=True)
    aoc.validate(aoc.part1(), 18)
    aoc.validate(aoc.part2(), 54)
    # Run against actual data
    aoc = AOC2022Day24(example=False)
    aoc.run()
