#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/9
'''
import re
import textwrap
from collections import defaultdict
from typing import Callable

# Local imports
from aoc import AOC


class AOC2015Day9(AOC):
    '''
    Day 9 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        London to Dublin = 464
        London to Belfast = 518
        Dublin to Belfast = 141
        '''
    )

    validate_part1: int = 605

    # Set by post_init
    distances = None

    def post_init(self) -> None:
        '''
        Load the distances
        '''
        distance_re: re.Pattern = re.compile(r'(\w+) to (\w+) = (\d+)')
        self.distances = defaultdict(dict)

        for line in self.input.splitlines():
            origin: str
            dest: str
            dist: str
            origin, dest, dist = distance_re.match(line).groups()
            self.distances[origin][dest] = self.distances[dest][origin] = int(dist)

    def dfs(self, strategy: Callable) -> int:
        '''
        Perform a depth-first search with the specified strategy
        '''
        if strategy not in (min, max):
            raise ValueError(f'Unsupported strategy: {strategy!r}')

        def _dfs(
            origin: str,
            visited: set | None = None,
            to_visit: set | None = None,
            total_dist: int = 0,
        ) -> int:
            '''
            Recursive function to implement DFS
            '''
            # Create distinct set of visited/to_visit cities for each branch
            visited = (visited if visited is not None else set()) | {origin}
            to_visit = (
                to_visit if to_visit is not None else set(self.distances)
            ) - visited

            if not to_visit:
                # All cities have been visited, return the full
                return total_dist

            result = None

            for dest in to_visit:
                new_dist = _dfs(
                    dest,
                    visited,
                    to_visit,
                    total_dist + self.distances[origin][dest],
                )
                try:
                    result = strategy(result, new_dist)
                except TypeError:
                    result = new_dist

            return result

        return strategy(_dfs(city) for city in self.distances)

    def part1(self) -> int:
        '''
        Return shortest distance
        '''
        return self.dfs(strategy=min)

    def part2(self) -> int:
        '''
        Return longest distance
        '''
        return self.dfs(strategy=max)


if __name__ == '__main__':
    aoc = AOC2015Day9()
    aoc.run()
