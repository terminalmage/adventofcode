#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/1
'''
import re
import textwrap
from collections import deque
from collections.abc import Iterator, Sequence

# Local imports
from aoc import AOC, TupleMixin, XY, directions

START: XY = (0, 0)

# Type hints
Step = tuple[str, int]


class AOC2016Day1(AOC, TupleMixin):
    '''
    Day 1 of Advent of Code 2016
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        R5, L5, R5, R3
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        R8, R4, R4, R8
        '''
    )

    validate_part1: int = 12
    validate_part2: int = 4

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

    def walk(self, steps: Sequence[Step]) -> Iterator[XY]:
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
    aoc = AOC2016Day1()
    aoc.run()
