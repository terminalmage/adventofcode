#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/14
'''
import itertools
import re
import math
import textwrap
from collections import defaultdict

# Local imports
from aoc import AOC, XY

# Type hints
Robot = list[int]
Robots = list[Robot]


class AOC2024Day14(AOC):
    '''
    Day 14 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        p=0,4 v=3,-3
        p=6,3 v=-1,-3
        p=10,3 v=-1,2
        p=2,0 v=2,-1
        p=0,0 v=1,3
        p=3,0 v=-2,-2
        p=7,6 v=-1,-3
        p=3,0 v=-1,-2
        p=9,3 v=2,3
        p=7,3 v=-1,2
        p=2,4 v=2,-3
        p=9,5 v=-3,-3
        '''
    )

    validate_part1: int = 12

    # Set by post_init
    robots = None
    cols = None
    rows = None
    col_edge = None
    row_edge = None

    def post_init(self) -> None:
        '''
        Set the bounds and discover the edges
        '''
        if self.example:
            self.cols = 11
            self.rows = 7
        else:
            self.cols = 101
            self.rows = 103

        self.col_edge = self.cols // 2
        self.row_edge = self.rows // 2

    def quadrant(self, x: int, y: int) -> int:
        '''
        Given a column x and row y, return the quadrant number (from 1 to 4)
        that the coordinate falls within. If it is on an edge, return 0.
        '''
        if x == self.col_edge or y == self.row_edge:
            return 0

        match (x > self.col_edge, y > self.row_edge):
            case (False, False):
                return 1
            case (False, True):
                return 2
            case (True, False):
                return 3
            case (True, True):
                return 4

    def load_robots(self) -> Robots:
        '''
        Load robots from puzzle input
        '''
        return [
            [px, py, vx, vy]
            for px, py, vx, vy in (
                map(int, re.findall(r'-?\d+', line))
                for line in self.input.splitlines()
            )
        ]

    def travel(self, robots: Robots, seconds: int) -> None:
        '''
        Simulate moving the robots for the specified number of seconds
        '''
        robot: Robot
        for robot in robots:
            robot[0] = (robot[0] + (robot[2] * seconds)) % self.cols
            robot[1] = (robot[1] + (robot[3] * seconds)) % self.rows

    def part1(self) -> int:
        '''
        Simulate movement for 100 seconds and return the product of the number
        of robots in each quadrant.
        '''
        robots: Robots = self.load_robots()
        self.travel(robots, seconds=100)

        buckets: defaultdict[int] = defaultdict(int)
        for robot in robots:
            buckets[self.quadrant(*robot[:2])] += 1

        return math.prod([buckets[n] for n in range(1, 5)])

    def part2(self) -> int:
        '''
        Simulate movement until the robots end up arranged in the shape of a
        Christmas tree. How are we supposed to know when this happens? No
        goddamn clue, but according to the subreddit this happens when all
        robots are in unique positions (i.e. no overlap). /me shrugs
        '''
        robots: Robots = self.load_robots()

        elapsed: int
        for elapsed in itertools.count(1):
            self.travel(robots, seconds=1)
            if len({(x[0], x[1]) for x in robots}) == len(robots):
                return elapsed


if __name__ == '__main__':
    aoc = AOC2024Day14()
    aoc.run()
