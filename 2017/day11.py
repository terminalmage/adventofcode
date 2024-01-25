#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/11
'''
import textwrap

# Local imports
from aoc import AOC


class AOC2017Day11(AOC):
    '''
    Day 11 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        se,sw,se,sw,sw
        '''
    )

    validate_part1: int = 3

    def post_init(self) -> None:
        '''
        Load the puzzle input and process the steps
        '''
        self.max_dist: int = 0

        q: int = 0
        r: int = 0
        s: int = 0

        # See https://www.redblobgames.com/grids/hexagons/#coordinates-cube
        step: str
        for step in self.input.split(','):
            match step:
                case 'n':
                    s += 1
                    r -= 1
                case 'ne':
                    q += 1
                    r -= 1
                case 'se':
                    q += 1
                    s -= 1
                case 's':
                    r += 1
                    s -= 1
                case 'sw':
                    r += 1
                    q -= 1
                case 'nw':
                    q -= 1
                    s += 1
                case _:
                    raise ValueError(f'Invalid step {step!r}')

            self.max_dist = max(self.max_dist, self.hex_dist(q, r, s))

        self.dist: int = self.hex_dist(q, r, s)

    @staticmethod
    def hex_dist(q: int, r: int, s: int) -> int:
        '''
        Compute the distance between cube coordinates
        '''
        return (abs(q) + abs(r) + abs(s)) // 2

    def part1(self) -> int:
        '''
        Return the hex distance from the start after following all the steps
        '''
        return self.dist

    def part2(self) -> int:
        '''
        Return the max distance at any point during the journey
        '''
        return self.max_dist


if __name__ == '__main__':
    aoc = AOC2017Day11()
    aoc.run()
