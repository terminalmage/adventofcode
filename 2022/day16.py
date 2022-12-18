#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/16
'''
from __future__ import annotations
import collections
import dataclasses
import functools
import re
from collections.abc import Sequence

# Local imports
from aoc2022 import AOC2022

TIME_LIMIT = 30


@dataclasses.dataclass
class Results:
    '''
    Dataclass to hold the results of a depth-first search
    '''
    pressure: int
    segments: dict[frozenset, int]


@dataclasses.dataclass
class Valve:
    '''
    Represents a single valve
    '''
    name: str
    rate: int
    neighbors: str | Sequence[str]
    distance_to: dict[str, int] = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        '''
        Split neighbors if passed as a string
        '''
        if isinstance(self.neighbors, str):
            self.neighbors = [
                item.strip() for item in self.neighbors.split(', ')
            ]

        for neighbor in self.neighbors:
            if not re.match('^[A-Z]+$', neighbor):
                raise ValueError(
                    f'Invalid neighbor {neighbor!r} for valve {self.name}'
                )


class AOC2022Day16(AOC2022):
    '''
    Day 16 of Advent of Code 2022
    '''
    day = 16

    def __init__(self, example: bool = False) -> None:
        '''
        Load the valve definitions
        '''
        super().__init__(example=example)

        self.valves = {}
        valve_def = re.compile(
            r'^Valve ([A-Z]+) has flow rate=(\d+); '
            r'tunnels? leads? to valves? ([A-Z, ]+)$'
        )
        self.start = 'AA'
        self.best = {}

        with self.input.open() as fh:
            for line in fh:
                name, rate, neighbors = valve_def.match(line.rstrip()).groups()
                self.valves[name] = Valve(
                    name=name, rate=int(rate), neighbors=neighbors
                )

        # Only stop at valves with a nonzero flow rate
        self.stops = tuple(
            item.name for item in self.valves.values()
            if item.rate or item.name == self.start
        )

    @functools.lru_cache
    def bfs(
        self,
        start: str,
        end: str,
    ) -> int:
        '''
        Use breadth-first search to find distance of shortest path
        '''
        visited = set()

        dq = collections.deque([(start, 0)])

        while dq:
            name, distance = dq.popleft()
            if name == end:
                return distance

            for neighbor in self.valves[name].neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dq.append((neighbor, distance + 1))

    def dfs(
        self,
        start: str,
        clock: int = TIME_LIMIT,
    ) -> Results:
        '''
        Perform a depth-first search to get the most pressure that can be
        released in the specified time
        '''
        path_segments = {}

        def _dfs(
            round_start: str,
            clock: int,
            visited: set,
            to_visit: set,
            pressure: int = 0,
        ):
            '''
            Recursive function to perform DFS
            '''
            # Create new distinct sets to use for this recursion level, unless no
            # set was passed, in which case initialize them.
            visited = visited | {round_start}
            to_visit = to_visit - visited

            # The current path traversed is the set of visited nodes minus the
            # original start point (i.e. not the start of the current round)
            path = frozenset(visited - {start})
            # Keep track of the pressure for different path segments
            path_segments[path] = max(path_segments.setdefault(path, 0), pressure)

            highest_pressure = 0

            for dest in to_visit:
                # Subtract the time to get from the current location to the
                # destination, and an extra second to open the valve
                new_clock = clock - self.bfs(*sorted((round_start, dest))) - 1
                if new_clock > 0:
                    # Add the pressure for the destination valve multiplied by
                    # the number of remaining seconds. For example, if we are
                    # opening a valve with flow_rate 10, and there are 17
                    # seconds remaining on the clock, it will contribute a
                    # cumulative pressure of 170 to the total.
                    new_pressure = self.valves[dest].rate * new_clock
                    # Recurse to add the largest cumulative flow from the
                    # remaining unvisited valves
                    new_pressure += _dfs(
                        dest,
                        new_clock,
                        visited,
                        to_visit,
                        pressure + new_pressure,
                    )
                    if new_pressure > highest_pressure:
                        highest_pressure = new_pressure

            return highest_pressure

        visited = set()
        to_visit = set(self.stops)
        pressure = _dfs(start, clock, visited, to_visit)

        return Results(pressure, path_segments)

    def part1(self) -> int:
        '''
        Calculate the max pressure that can be released in the allotted time
        '''
        return self.dfs(start=self.start).pressure

    def part2(self) -> int:
        '''
        Calculate the max pressure that can be released in the allotted time
        '''
        # Gather the best flow for the paths traversed in the "ideal" path
        path_segments = self.dfs(start=self.start, clock=TIME_LIMIT - 4).segments

        def _visit_remaining_path_segments(segment: frozenset | None):
            '''
            Recursively calculate the flow rate for subsegments of the "ideal"
            path. This lets us know the ideal next move for both parties, given
            whatever the current state of visited valves may be.
            '''
            if segment not in path_segments:
                max_pressure = 0
                # Get the max pressure for this segment and subsegments
                for valve in segment:
                    subsegment = segment - {valve}
                    max_pressure = max(
                        max_pressure,
                        _visit_remaining_path_segments(subsegment),
                    )
                path_segments[segment] = max_pressure

            # Return the max pressure for this subsegment to the caller
            return path_segments[segment]

        #import pprint
        #pprint.pprint(path_segments)
        # Now get the rest of the paths
        _visit_remaining_path_segments(frozenset(set(self.stops) - {self.start}))

        # Finally, iterate over the valves with nonzero flow, using the data we
        # gathered above in path_segments to determine the highest amount of
        # pressure that could be released. Start with the elephant visiting
        # zero rooms, and end with the elephant visiting (almost) all rooms
        max_pressure = 0
        for my_path in path_segments:
            # path_segments is keyed by frozenset
            elephant_path = frozenset(set(self.stops) - my_path - {'AA'})
            max_pressure = max(
                max_pressure,
                path_segments[my_path] + path_segments[elephant_path]
            )

        return max_pressure



if __name__ == '__main__':
    aoc = AOC2022Day16(example=False)
    print(f'Answer 1: {aoc.part1()}')
    print(f'Answer 2: {aoc.part2()}')
