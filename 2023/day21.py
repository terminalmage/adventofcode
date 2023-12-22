#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/21
'''
import collections
import math

# Local imports
from aoc import AOC, Coordinate, Grid, InfiniteGrid


class AOC2023Day21(AOC):
    '''
    Day 21 of Advent of Code 2023
    '''
    day = 21

    def bfs(
        self,
        grid: Grid | InfiniteGrid,
        start: Coordinate,
        steps: int,
    ) -> int:
        '''
        Use breadth-first search to find max number of garden plots that can be
        visited in the specified number of steps
        '''
        if steps < 1:
            raise ValueError('Steps must be > 0')

        visited = set()
        garden_plots = 0

        # Since we need to travel a specific number of steps, we can simply
        # check if the number if steps is even or odd, and disregard any
        # destinations which are not also even/odd.
        even_odd = steps % 2

        dq = collections.deque([(start, 0)])
        while dq:
            coord, steps_traveled  = dq.popleft()

            # Don't exceed max steps or retrace a previous movement; If a
            # coordinate is in the set of coordinates that we've visited, we
            # will already have queued up all the possible directional
            # movements one could make from that position.
            if steps_traveled > steps or coord in visited:
                continue

            visited.add(coord)

            if steps_traveled % 2 == even_odd:
                # Valid stopping point
                garden_plots += 1

            for new_coord, tile in grid.neighbors(coord):
                if tile != '#':
                    dq.append((new_coord, steps_traveled + 1))

        return garden_plots

    def part1(self) -> int:
        '''
        Return the number of garden plots reachable in exactly the specified
        number of steps.
        '''
        garden = Grid(self.input)
        return self.bfs(
            grid=garden,
            start=garden.find('S'),
            steps=6 if self.example else 64,
        )

    def part2(self) -> int:
        '''
        Return the number of garden plots reachable in exactly the specified
        number of steps.
        '''
        steps = 26501365
        garden = InfiniteGrid(self.input)
        start = garden.find('S')

        # Perform quadratic interpolation. First, get number of plots reachable
        # with 65 + (height/width * x) for 0 <= x <= 2.
        u1, u2, u3 = (
            self.bfs(garden, start, 65 + garden.rows * x)
            for x in range(3)
        )

        # Get differential between first two numbers
        diff1 = u2 - u1
        # Get 2nd level differential (diff between 3 and 2, minus first diff)
        diff2 = u3 - u2 - diff1

        # 2a = diff2
        a = diff2 // 2
        # 3a + b = diff1
        b = diff1 - (3 * a)
        # a + b + c = u1
        c = u1 - a - b
        # Number of grids we need to travel
        n = math.ceil(steps / garden.rows)

        return (a * n**2) + (b * n) + c


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day21(example=True)
    aoc.validate(aoc.part1(), 16)
    # Run against actual data
    aoc = AOC2023Day21(example=False)
    aoc.run()
