#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/24
'''
from __future__ import annotations
import functools
import itertools
import textwrap
from collections import defaultdict

# Local imports
from aoc import AOC

Component = tuple[int, int]
Components = dict[int, list[int]]
Bridge = list[Component]


class AOC2017Day24(AOC):
    '''
    Day 24 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        0/2
        2/2
        2/3
        3/4
        3/5
        0/1
        10/1
        9/10
        '''
    )

    validate_part1: int = 31
    validate_part2: int = 19

    def load_components(self) -> Components:
        '''
        Load the input data into a data structure
        '''
        components: Components = defaultdict(set)
        for line in self.input.splitlines():
            side1: int
            side2: int
            side1, side2 = (int(s) for s in line.split('/'))
            components[side1].add(side2)
            components[side2].add(side1)
        return components

    @functools.cached_property
    def bridges(self) -> int:
        '''
        Get all bridges
        '''
        components = self.load_components()

        def _dfs(cur_bridge: Bridge | None = None):
            '''
            Recursive generator that returns possible bridges that can be
            constructed from the given components
            '''
            # Start with (0, 0) if no bridge parameters are specified, to
            # ensure that:
            #
            #   1. The first component we add to the bridge starts with a 0
            #   2. We don't add numeric value to the bridge, which would
            #      interfere with computing strength.
            #
            cur_bridge = cur_bridge or [(0, 0)]
            # Outward-facing port of the last component in the bridge. We'll
            # use this to pick possible components that can connect to it.
            port = cur_bridge[-1][1]
            # Try each of the values associated with the
            matching: int
            for matching in components[port]:
                if not any(
                    comp in cur_bridge
                    for comp in itertools.permutations((port, matching))
                ):
                    extended: Bridge = cur_bridge + [(port, matching)]
                    yield tuple(extended)
                    yield from _dfs(extended)

        return list(_dfs())

    @staticmethod
    def strength(bridge: Bridge) -> int:
        '''
        Return the strength for a given Bridge
        '''
        return sum(sum(comp) for comp in bridge)

    def part1(self) -> int:
        '''
        Return the strength of the strongest possible bridge which can be
        created with the components from the puzzle input.
        '''
        return max(self.strength(bridge) for bridge in self.bridges)

    def part2(self) -> int:
        '''
        Return the strength of the longest bridge
        '''
        bridges: dict[int, list[Bridge]] = defaultdict(set)
        for bridge in self.bridges:
            bridges[len(bridge)].add(tuple(bridge))

        return max(
            self.strength(bridge)
            for bridge in bridges[max(bridges)]
        )


if __name__ == '__main__':
    aoc = AOC2017Day24()
    aoc.run()
