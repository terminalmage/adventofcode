#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/16

--- Day 16: Proboscidea Volcanium ---

The sensors have led you to the origin of the distress signal: yet another
handheld device, just like the one the Elves gave you. However, you don't see
any Elves around; instead, the device is surrounded by elephants! They must
have gotten lost in these tunnels, and one of the elephants apparently figured
out how to turn on the distress signal.

The ground rumbles again, much stronger this time. What kind of cave is this,
exactly? You scan the cave with your handheld device; it reports mostly igneous
rock, some ash, pockets of pressurized gas, magma... this isn't just a cave,
it's a volcano!

You need to get the elephants out of here, quickly. Your device estimates that
you have 30 minutes before the volcano erupts, so you don't have time to go
back out the way you came in.

You scan the cave for other options and discover a network of pipes and
pressure-release valves. You aren't sure how such a system got into a volcano,
but you don't have time to complain; your device produces a report (your puzzle
input) of each valve's flow rate if it were opened (in pressure per minute) and
the tunnels you could use to move between the valves.

There's even a valve in the room you and the elephants are currently standing
in labeled AA. You estimate it will take you one minute to open a single valve
and one minute to follow any tunnel from one valve to another. What is the most
pressure you could release?

For example, suppose you had the following scan output:

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

All of the valves begin closed. You start at valve AA, but it must be damaged
or jammed or something: its flow rate is 0, so there's no point in opening it.
However, you could spend one minute moving to valve BB and another minute
opening it; doing so would release pressure during the remaining 28 minutes at
a flow rate of 13, a total eventual pressure release of 28 * 13 = 364. Then,
you could spend your third minute moving to valve CC and your fourth minute
opening it, providing an additional 26 minutes of eventual pressure release at
a flow rate of 2, or 52 total pressure released by valve CC.

Making your way through the tunnels like this, you could probably open many or
all of the valves by the time 30 minutes have elapsed. However, you need to
release as much pressure as possible, so you'll need to be methodical. Instead,
consider this approach:

== Minute 1 ==
No valves are open.
You move to valve DD.

== Minute 2 ==
No valves are open.
You open valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You move to valve CC.

== Minute 4 ==
Valve DD is open, releasing 20 pressure.
You move to valve BB.

== Minute 5 ==
Valve DD is open, releasing 20 pressure.
You open valve BB.

== Minute 6 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve AA.

== Minute 7 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve II.

== Minute 8 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve JJ.

== Minute 9 ==
Valves BB and DD are open, releasing 33 pressure.
You open valve JJ.

== Minute 10 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve II.

== Minute 11 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve AA.

== Minute 12 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve DD.

== Minute 13 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve EE.

== Minute 14 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve FF.

== Minute 15 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve GG.

== Minute 16 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve HH.

== Minute 17 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You open valve HH.

== Minute 18 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve GG.

== Minute 19 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve FF.

== Minute 20 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve EE.

== Minute 21 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve EE.

== Minute 22 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve DD.

== Minute 23 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve CC.

== Minute 24 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You open valve CC.

== Minute 25 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 27 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 28 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 29 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 30 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

This approach lets you release the most pressure possible in 30 minutes with
this valve layout, 1651.

Work out the steps to release the most pressure in 30 minutes. What is the most
pressure you can release?

--- Part Two ---

You're worried that even with an optimal approach, the pressure released won't
be enough. What if you got one of the elephants to help you?

It would take you 4 minutes to teach an elephant how to open the right valves
in the right order, leaving you with only 26 minutes to actually execute your
plan. Would having two of you working together be better, even if it means
having less time? (Assume that you teach the elephant before opening any valves
yourself, giving you both the same full 26 minutes.)

In the example above, you could teach the elephant to help you as follows:

== Minute 1 ==
No valves are open.
You move to valve II.
The elephant moves to valve DD.

== Minute 2 ==
No valves are open.
You move to valve JJ.
The elephant opens valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You open valve JJ.
The elephant moves to valve EE.

== Minute 4 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve II.
The elephant moves to valve FF.

== Minute 5 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve AA.
The elephant moves to valve GG.

== Minute 6 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve BB.
The elephant moves to valve HH.

== Minute 7 ==
Valves DD and JJ are open, releasing 41 pressure.
You open valve BB.
The elephant opens valve HH.

== Minute 8 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve CC.
The elephant moves to valve GG.

== Minute 9 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve CC.
The elephant moves to valve FF.

== Minute 10 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant moves to valve EE.

== Minute 11 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant opens valve EE.

(At this point, all valves are open.)

== Minute 12 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 20 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.


With the elephant helping, after 26 minutes, the best you could do would
release a total of 1707 pressure.

With you and an elephant working together for 26 minutes, what is the most
pressure you could release?
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
    Base class for Day 16 of Advent of Code 2022
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
