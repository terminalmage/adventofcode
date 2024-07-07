#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/16
'''
from __future__ import annotations
import functools
import re
import textwrap
from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass, field

# Local imports
from aoc import AOC

TIME_LIMIT: int = 30


@dataclass
class Results:
    '''
    Dataclass to hold the results of a depth-first search
    '''
    pressure: int
    segments: dict[frozenset, int]


@dataclass
class Valve:
    '''
    Represents a single valve
    '''
    name: str
    rate: int
    neighbors: str | Sequence[str]
    distance_to: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        '''
        Split neighbors if passed as a string
        '''
        if isinstance(self.neighbors, str):
            self.neighbors: list[str] = [
                item.strip() for item in self.neighbors.split(', ')
            ]

        neighbor: str
        for neighbor in self.neighbors:
            if not re.match('^[A-Z]+$', neighbor):
                raise ValueError(
                    f'Invalid neighbor {neighbor!r} for valve {self.name}'
                )


class AOC2022Day16(AOC):
    '''
    Day 16 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        Valve BB has flow rate=13; tunnels lead to valves CC, AA
        Valve CC has flow rate=2; tunnels lead to valves DD, BB
        Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
        Valve EE has flow rate=3; tunnels lead to valves FF, DD
        Valve FF has flow rate=0; tunnels lead to valves EE, GG
        Valve GG has flow rate=0; tunnels lead to valves FF, HH
        Valve HH has flow rate=22; tunnel leads to valve GG
        Valve II has flow rate=0; tunnels lead to valves AA, JJ
        Valve JJ has flow rate=21; tunnel leads to valve II
        '''
    )

    validate_part1: int = 1651
    validate_part2: int = 1707

    # Set by post_init
    valves = None
    start = None
    best = None
    stops = None

    def post_init(self) -> None:
        '''
        Load the valve definitions
        '''
        self.valves: dict[str, Valve] = {}
        valve_def: re.Pattern = re.compile(
            r'^Valve ([A-Z]+) has flow rate=(\d+); '
            r'tunnels? leads? to valves? ([A-Z, ]+)$'
        )
        self.start: str = 'AA'
        self.best = {}  # MAYBE REMOVE

        for line in self.input.splitlines():
            name: str
            rate: str
            neighbors: str
            name, rate, neighbors = valve_def.match(line).groups()
            self.valves[name] = Valve(
                name=name, rate=int(rate), neighbors=neighbors
            )

        # Only stop at valves with a nonzero flow rate
        self.stops: tuple[str, ...] = tuple(
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
        visited: set[str] = set()

        dq: deque[tuple[str, int]] = deque([(start, 0)])

        name: str
        distance: int
        neighbor: str

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
            visited: set[str],
            to_visit: set[str],
            pressure: int = 0,
        ):
            '''
            Recursive function to perform DFS
            '''
            # Create new distinct sets to use for this recursion level, unless no
            # set was passed, in which case initialize them.
            visited: set[str] = visited | {round_start}
            to_visit: set[str] = to_visit - visited

            # The current path traversed is the set of visited nodes minus the
            # original start point (i.e. not the start of the current round)
            path: frozenset[str] = frozenset(visited - {start})
            # Keep track of the pressure for different path segments
            path_segments[path] = max(path_segments.setdefault(path, 0), pressure)

            highest_pressure: int = 0

            dest: str
            for dest in to_visit:
                # Subtract the time to get from the current location to the
                # destination, and an extra second to open the valve
                new_clock: int = clock - self.bfs(*sorted((round_start, dest))) - 1
                if new_clock > 0:
                    # Add the pressure for the destination valve multiplied by
                    # the number of remaining seconds. For example, if we are
                    # opening a valve with flow_rate 10, and there are 17
                    # seconds remaining on the clock, it will contribute a
                    # cumulative pressure of 170 to the total.
                    new_pressure: int = self.valves[dest].rate * new_clock
                    # Recurse to add the largest cumulative flow from the
                    # remaining unvisited valves
                    new_pressure += _dfs(
                        dest,
                        new_clock,
                        visited,
                        to_visit,
                        pressure + new_pressure,
                    )
                    highest_pressure = max(new_pressure, highest_pressure)

            return highest_pressure

        visited: set[str] = set()
        to_visit: set[str] = set(self.stops)
        pressure: int = _dfs(start, clock, visited, to_visit)

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
        path_segments: dict[frozenset[str], int] = self.dfs(
            start=self.start,
            clock=TIME_LIMIT - 4,
        ).segments

        def _visit_remaining_path_segments(segment: frozenset[str] | None):
            '''
            Recursively calculate the flow rate for subsegments of the "ideal"
            path. This lets us know the ideal next move for both parties, given
            whatever the current state of visited valves may be.
            '''
            if segment not in path_segments:
                max_pressure: int = 0
                # Get the max pressure for this segment and subsegments
                for valve in segment:
                    subsegment: frozenset[str] = segment - {valve}
                    max_pressure: int = max(
                        max_pressure,
                        _visit_remaining_path_segments(subsegment),
                    )
                path_segments[segment] = max_pressure

            # Return the max pressure for this subsegment to the caller
            return path_segments[segment]

        # Now get the rest of the paths
        _visit_remaining_path_segments(frozenset(set(self.stops) - {self.start}))

        # Finally, iterate over the valves with nonzero flow, using the data we
        # gathered above in path_segments to determine the highest amount of
        # pressure that could be released. Start with the elephant visiting
        # zero rooms, and end with the elephant visiting (almost) all rooms
        max_pressure: int = 0
        my_path: frozenset[str]
        for my_path in path_segments:
            # path_segments is keyed by frozenset
            elephant_path: frozenset[str] = frozenset(set(self.stops) - my_path - {'AA'})
            max_pressure: int = max(
                max_pressure,
                path_segments[my_path] + path_segments[elephant_path]
            )

        return max_pressure


if __name__ == '__main__':
    aoc = AOC2022Day16()
    aoc.run()
