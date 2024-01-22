#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/1
'''
import re
from collections import deque
from collections.abc import Generator, Sequence

# Local imports
from aoc import AOC, TupleMixin, XY, directions

START: XY = (0, 0)

# Type hints
Step = tuple[str, int]


class AOC2016Day1(AOC, TupleMixin):
    '''
    Day 1 of Advent of Code 2016
    '''
    def load_directions(self, data: str) -> tuple[Step]:
        '''
        Load the instructions
        '''
        return tuple(
            (m.group(1), int(m.group(2)))
            for m in re.finditer(r'([RL])(\d+),?', data)
        )

    @staticmethod
    def distance(end: XY, start: XY = START) -> int:
        '''
        Return the shortest distance in steps between two coordinates
        '''
        return sum(abs(x - y) for x, y in zip(end, start))

    def walk(self, steps: Sequence[Step]) -> Generator[XY, None, None]:
        '''
        Follow the directions, and then return the shortest number of steps
        to get to the destination.
        '''
        location = START
        deltas: deque[XY] = deque(
            (
                directions.NORTH,
                directions.EAST,
                directions.SOUTH,
                directions.WEST,
            )
        )
        turn: str
        distance: int
        for turn, distance in steps:
            deltas.rotate(1 if turn == 'L' else -1)
            for _ in range(distance):
                location: XY = self.tuple_add(location, deltas[0])
                yield location

    def part1(self) -> int:
        '''
        Return the distance from the starting point
        '''
        steps: tuple[Step] = self.load_directions(self.input_part1)
        return self.distance(list(self.walk(steps))[-1])

    def part2(self) -> int:
        '''
        Return the distance from the first location visited twice
        '''
        steps: tuple[Step] = self.load_directions(self.input_part2)
        visited: set[XY] = set()
        for location in self.walk(steps):
            if location in visited:
                return self.distance(location)
            visited.add(location)

        raise RuntimeError('Failed to find solution')


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day1(example=True)
    aoc.validate(aoc.part1(), 12)
    aoc.validate(aoc.part2(), 4)
    # Run against actual data
    aoc = AOC2016Day1(example=False)
    aoc.run()
