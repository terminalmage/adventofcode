#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/14

--- Day 14: Reindeer Olympics ---

This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must
rest occasionally to recover their energy. Santa would like to know which of
his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed) or resting (not
moving at all), and always spend whole seconds in either state.

For example, suppose you have the following Reindeer:

Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

After one second, Comet has gone 14 km, while Dancer has gone 16 km. After ten
seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh
second, Comet begins resting (staying at 140 km), and Dancer continues on for a
total distance of 176 km. On the 12th second, both reindeer are resting. They
continue to rest until the 138th second, when Comet flies for another ten
seconds. On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting, and Comet
is in the lead at 1120 km (poor Dancer has only gotten 1056 km by that point).
So, in this situation, Comet would win (if the race ended at 1000 seconds).

Given the descriptions of each reindeer (in your puzzle input), after exactly
2503 seconds, what distance has the winning reindeer traveled?

--- Part Two ---

Seeing how reindeer move in bursts, Santa decides he's not pleased with the old
scoring system.

Instead, at the end of each second, he awards one point to the reindeer
currently in the lead. (If there are multiple reindeer tied for the lead, they
each get one point.) He keeps the traditional 2503 second time limit, of
course, as doing otherwise would be entirely ridiculous.

Given the example reindeer from above, after the first second, Dancer is in the
lead and gets one point. He stays in the lead until several seconds into
Comet's second burst: after the 140th second, Comet pulls into the lead and
gets his first point. Of course, since Dancer had been in the lead for the 139
seconds before that, he has accumulated 139 points by the 140th second.

After the 1000th second, Dancer has accumulated 689 points, while poor Comet,
our old champion, only has 312. So, with the new scoring system, Dancer would
win (if the race ended at 1000 seconds).

Again given the descriptions of each reindeer (in your puzzle input), after
exactly 2503 seconds, how many points does the winning reindeer have?
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
