#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/10
'''
import re
from dataclasses import dataclass

# Local imports
from aoc import AOC, XY


@dataclass
class Point:
    '''
    Represents a single point, with its position and velocity
    '''
    x: int
    y: int
    vx: int
    vy: int

    def advance(self) -> None:
        '''
        Move the point by one factor of its velocity
        '''
        self.x += self.vx
        self.y += self.vy


class AOC2018Day10(AOC):
    '''
    Day 10 of Advent of Code 2018
    '''
    @staticmethod
    def render(points) -> str:
        '''
        Render the points into a string
        '''
        coords: set[XY] = {(p.x, p.y) for p in points}
        cols: set[int]
        rows: set[int]

        cols, rows = (set(n) for n in zip(*coords))
        lines: list[str] = []

        for row in range(min(rows), max(rows) + 1):
            line: str = ''
            for col in range(min(cols), max(cols) + 1):
                line += '#' if (col, row) in coords else ' '
            lines.append(line)

        return '\n'.join(lines) + '\n'

    def solve(self) -> None:
        '''
        Keep advancing the points until the height is <= 10, then render the
        resulting points and print the number of seconds it would take to get
        to that position.
        '''
        points: list[Point] = [
            Point(*(int(n) for n in re.findall(r'-?\d+', line)))
            for line in self.input.splitlines()
        ]
        seconds: int = 0

        while True:
            for point in points:
                point.advance()
            seconds += 1

            rows: set[int] = {p.y for p in points}
            height: int = max(rows) - min(rows)
            if height <= 10:
                print(self.render(points))
                print(f'Took {seconds} seconds')
                break


if __name__ == '__main__':
    aoc = AOC2018Day10()
    aoc.run()
    aoc.solve()
