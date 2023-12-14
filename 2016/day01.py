#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/1
'''
import collections
import re
from collections.abc import Generator, Sequence

# Local imports
from aoc import AOC

# Typing shortcuts
Coordinate = tuple[int]
Step = tuple[str, int]

START = (0, 0)


class AOC2016Day1(AOC):
    '''
    Day 1 of Advent of Code 2016
    '''
    day = 1

    def load_directions(self, part: int) -> tuple[Step]:
        '''
        Load the instructions
        '''
        return tuple(
            (m.group(1), int(m.group(2)))
            for m in re.finditer(
                r'([RL])(\d+),?',
                self.get_input(part=part).read_text()
            )
        )

    @staticmethod
    def distance(end: Coordinate, start: Coordinate = START) -> int:
        '''
        Return the shortest distance in steps between two coordinates
        '''
        return sum(abs(x - y) for x, y in zip(end, start))

    @staticmethod
    def walk(steps: Sequence[Step]) -> Generator[Coordinate, None, None]:
        '''
        Follow the directions, and then return the shortest number of steps
        to get to the destination.
        '''
        location = START
        deltas = collections.deque(
            (
                (0, 1),     # North
                (1, 0),     # East
                (0, -1),    # South
                (-1, 0),    # West
            )
        )
        for turn, distance in steps:
            deltas.rotate(1 if turn == 'L' else -1)
            for _ in range(distance):
                location = tuple(
                    a + b for a, b in zip(location, deltas[0])
                )
                yield location

    def part1(self) -> int:
        '''
        Return the distance from the starting point
        '''
        directions = self.load_directions(part=1)
        return self.distance(list(self.walk(directions))[-1])

    def part2(self) -> int:
        '''
        Return the distance from the first location visited twice
        '''
        directions = self.load_directions(part=2)
        visited = set()
        for location in self.walk(directions):
            if location in visited:
                return self.distance(location)
            visited.add(location)
        return 0


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day1(example=True)
    aoc.validate(aoc.part1(), 12)
    aoc.validate(aoc.part2(), 4)
    # Run against actual data
    aoc = AOC2016Day1(example=False)
    aoc.run()
