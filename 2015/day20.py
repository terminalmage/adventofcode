#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/20
'''
import math
from collections.abc import Callable, Generator

# Local imports
from aoc import AOC


class AOC2015Day20(AOC):
    '''
    Day 20 of Advent of Code 2015
    '''
    day = 20
    goal = 36000000

    @staticmethod
    def factors(
        number: int,
        limit: int | None = None,
    ) -> Generator[int, None, None]:
        '''
        Generator function to return the factors of a number
        '''
        for candidate in range(
            1,
            limit + 1 if limit else int(math.sqrt(number)),
        ):
            if number % candidate == 0:
                yield candidate
                complement = number // candidate
                if not limit or complement <= limit:
                    yield complement

    def find_house(self, condition: Callable[[int], int]) -> int:
        '''
        Given the passed callable defining the algorithm for calculating the
        number of presents that a given house will receive, return the loweste
        house number that will receive the desired number of presents.
        '''
        for house in range(100000, self.goal):
            if condition(house):
                return house

        raise RuntimeError('Something went wrong')

    def part1(self) -> int:
        '''
        Return the lowest house number that receives at least the goal number
        of presents.
        '''
        return self.find_house(
            lambda house: (10 * sum(self.factors(house))) >= self.goal
        )

    def part2(self) -> int:
        '''
        Return the lowest house number that receives at least the goal number
        of presents.
        '''
        return self.find_house(
            lambda house: (11 * sum(house // factor for factor in self.factors(house, limit=50))) >= self.goal
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day20(example=True)
    # Run against actual data
    aoc = AOC2015Day20(example=False)
    aoc.run()
