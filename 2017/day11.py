#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/11
'''
# Local imports
from aoc import AOC


class AOC2017Day11(AOC):
    '''
    Day 11 of Advent of Code 2017
    '''
    day = 11

    def __init__(self, example: bool = False) -> None:
        '''
        Load the puzzle input and process the steps
        '''
        super().__init__(example=example)

        self.max_dist: int = 0

        q: int = 0
        r: int = 0
        s: int = 0

        # See https://www.redblobgames.com/grids/hexagons/#coordinates-cube
        step: str
        for step in self.input.read_text().strip().split(','):
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
    # Run against test data
    aoc = AOC2017Day11(example=True)
    aoc.validate(aoc.part1(), 3)
    # Run against actual data
    aoc = AOC2017Day11(example=False)
    aoc.run()
