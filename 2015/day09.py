#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/9

--- Day 9: All in a Single Night ---

Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided
him the distances between every pair of locations. He can start and end at any
two (different) locations he wants, but he must visit each location exactly
once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141

The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982

The shortest of these is London -> Dublin -> Belfast = 605, and so the answer
is 605 in this example.

What is the distance of the shortest route?

--- Part Two ---

The next year, just to show off, Santa decides to take the route with the
longest distance instead.

He can still start and end at any two (different) locations he wants, and he
still must visit each location exactly once.

For example, given the distances above, the longest route would be 982 via (for
example) Dublin -> London -> Belfast.

What is the distance of the longest route?
'''
import re
from collections import defaultdict
from typing import Callable

# Local imports
from aoc import AOC


class AOC2015Day9(AOC):
    '''
    Day 9 of Advent of Code 2015
    '''
    day = 9

    def __init__(self, example: bool = False) -> None:
        '''
        Load the instructions
        '''
        super().__init__(example=example)

        distance_re = re.compile(r'(\w+) to (\w+) = (\d+)')
        self.distances = defaultdict(dict)

        with self.input.open() as fh:
            for line in fh:
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
    # Run against test data
    aoc = AOC2015Day9(example=True)
    aoc.validate(aoc.part1(), 605)
    #aoc.validate(aoc.part2(), None)
    # Run against actual data
    aoc = AOC2015Day9(example=False)
    aoc.run()
