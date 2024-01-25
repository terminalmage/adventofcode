#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/14
'''
import itertools
import re
import textwrap
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
    example_data: str = textwrap.dedent(
        '''
        Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
        Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
        '''
    )

    validate_part1: int = 1120
    validate_part2: int = 689

    def post_init(self) -> None:
        '''
        Load the instructions
        '''
        self.duration: int = 1000 if self.example else 2503
        reindeer_re: re.Pattern = re.compile(
            r'^(\w+) can fly (\d+) km/s for (\d+) seconds.+ for (\d+) seconds'
        )

        self.reindeer = tuple(
            Reindeer(
                reindeer.group(1),
                *(int(group) for group in reindeer.groups()[1:])
            )
            for reindeer in (
                reindeer_re.match(line) for line in self.input.splitlines()
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
            leading_distance: int = max(item.distance for item in self.reindeer)
            # Increment all reindeer with the winning distance
            for reindeer, meta in scoreboard.items():
                if reindeer.distance == leading_distance:
                    meta['score'] += 1

        return max(item['score'] for item in scoreboard.values())


if __name__ == '__main__':
    aoc = AOC2015Day14()
    aoc.run()
