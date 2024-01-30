#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/20
'''
from collections.abc import Callable

# Local imports
from aoc import AOC, MathMixin


class AOC2015Day20(AOC, MathMixin):
    '''
    Day 20 of Advent of Code 2015
    '''
    def post_init(self) -> None:
        '''
        Convert the value in the input data to an int
        '''
        self.goal: int = int(self.input)

    def find_house(self, condition: Callable[[int], int]) -> int:
        '''
        Given the passed callable defining the algorithm for calculating the
        number of presents that a given house will receive, return the loweste
        house number that will receive the desired number of presents.
        '''
        house: int
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
            lambda house: (
                11 * sum(
                    house // factor
                    for factor in self.factors(house, limit=50)
                )
            ) >= self.goal
        )


if __name__ == '__main__':
    aoc = AOC2015Day20()
    aoc.run()
