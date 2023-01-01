#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/14
'''
import itertools
import re
from collections.abc import Iterator

# Local imports
from aoc import AOC


class Reindeer:
    '''
    Contains information about a reindeer
    '''
    def __init__(
        self,
        name: str,
        speed: int,
        active_time: int,
        rest_time: int,
    ) -> None:
        '''
        Initialize a Reindeer
        '''
        self.name = name
        self.speed = speed
        self.active_time = active_time
        self.rest_time = rest_time
        self.distance = 0

    def __repr__(self) -> str:
        '''
        Define the repr() output
        '''
        return (
            f'Reindeer(name={self.name!r}, speed={self.speed}, '
            f'active_time={self.active_time}, rest_time={self.rest_time}, '
            f'distance={self.distance})'
        )

    @property
    def flightplan(self) -> Iterator[int]:
        '''
        Returns a sequence of distances for each second of flight, and
        maintains a running count of the current total distance traveled
        '''
        self.distance = 0
        flightplan = itertools.cycle(
            ((self.speed,) * self.active_time) + ((0,) * self.rest_time)
        )
        while True:
            distance = next(flightplan)
            self.distance += distance
            yield distance


class AOC2015Day14(AOC):
    '''
    Day 14 of Advent of Code 2015
    '''
    day = 14

    def __init__(self, example: bool = False) -> None:
        '''
        Load the instructions
        '''
        super().__init__(example=example)
        self.duration = 1000 if self.example else 2503
        reindeer_re = re.compile(
            r'^(\w+) can fly (\d+) km/s for (\d+) seconds.+ for (\d+) seconds'
        )

        with self.input.open() as fh:
            self.reindeer = tuple(
                Reindeer(
                    reindeer.group(1),
                    *(int(group) for group in reindeer.groups()[1:])
                )
                for reindeer in (
                    reindeer_re.match(line) for line in fh
                )
            )

    def part1(self) -> int:
        '''
        Return max distance traveled
        '''
        return max(
            sum(itertools.islice(reindeer.flightplan, self.duration))
            for reindeer in self.reindeer
        )

    def part2(self) -> int:
        '''
        Return number of points won by the winning reindeer
        '''
        scoreboard = {
            reindeer: {
                'flightplan': reindeer.flightplan,
                'score': 0,
            }
            for reindeer in self.reindeer
        }

        for _ in range(self.duration):
            # Simulate one second of flight
            for reindeer in self.reindeer:
                next(scoreboard[reindeer]['flightplan'])
            # Get the max distance
            leading_distance = max(item.distance for item in self.reindeer)
            # Increment all reindeer with the winning distance
            for reindeer, meta in scoreboard.items():
                if reindeer.distance == leading_distance:
                    meta['score'] += 1

        return max(item['score'] for item in scoreboard.values())


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day14(example=True)
    aoc.validate(aoc.part1(), 1120)
    aoc.validate(aoc.part2(), 689)
    # Run against actual data
    aoc = AOC2015Day14(example=False)
    aoc.run()
