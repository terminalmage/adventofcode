#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/21
'''
import collections

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

        # Because the pattern has clear edges and a direct route to the edge,
        # we know that the number of reachable plots will grow quadratically
        # every grid-width columns, starting at the edge of the initial grid.
        # For a quadratic sequence in the format an² + bn + c, the variable c
        # would represent the number of plots reachable in the number of steps
        # needed to reach the edge (proof for this can be found below), while
        # the growth factor per grid (n) would be represented by an² + bn.
        #
        # The values for a and b can be calculated using quadratic
        # interpolation, given the first 3 numbers in the quadratic sequence.
        # To calculate the first three numbers, we can simply re-run our BFS
        # algorithm on our InfiniteGrid to get the number of plots for 0, 1 and
        # 2 full grid-width from the edge. We will refer to these three numbers
        # as u₀, u₁, u₂, stored here as variables u0, u1, and u2 because
        # subscripts are not valid characters in Python variable names. :)
        edge = garden.max_col - start[1]
        u0, u1, u2 = (
            self.bfs(garden, start, edge + (garden.cols * x))
            for x in range(3)
        )

        # Derive a, b, and c for the quadratic f(n) = an² + bn + c
        #
        # First, derive c. We can do this by substituting 0 for n, the rvalue
        # of which should be equal to u₀. This results in the following:
        #
        # (a * 0²) + (b * 0) + c = u₀
        #
        # On the left side, both of the first two parentheticals zero out,
        # leaving c as being equal to u₀. As mentioned earlier, this is simply
        # the number of reachable plots available within the number of steps
        # between the starting point and the edge of the grid (at which point
        # growth will increase quadratically).
        c = u0

        # Next, derive b. Evaluate f(n) for n=1, the rvalue of which should be
        # equal to u₁. In place of c, substitute our derived value u₀. The
        # result is shown below:
        #
        # (a * 1²) + (b * 1) + u₀ = u₁
        # a + b = u₁ - u₀
        # b = u₁ - u₀ - a
        #
        # We can't calculate b yet, but we can use the formula we just derived
        # for b to derive a. Evaluate f(n) for n=2 (again substituting our
        # derived value for c), the result of which should be equal to u₂:
        #
        # (a * 2²) + (b * 2) + u₀ = u₂
        # 4a + 2b = u₂ - u₀
        #
        # Substituting our derived value for b (i.e. u₁ - u₀ - a), we get:
        #
        # 4a + (2 * (u₁ - u₀ - a)) = u₂ - u₀
        # 4a + 2u₁ - 2u₀ - 2a = u₂ - u₀
        # 2a + 2u₁ - 2u₀ = u₂ - u₀
        # 2a = u₂ - u₀ - 2u₁ + 2u₀
        # 2a = u₂ - 2u₁ + u₀
        # a = (u₂ - 2u₁ + u₀) / 2
        a = (u2 - (2 * u1) + u0) // 2

        # With a calculated value for a, we can plug that in to our formula we
        # made to derive b above:
        b = u1 - u0 - a

        # Number of grid widths we need to travel after reaching the edge
        # (note: this is also an integer, given that the edge is 65 columns
        # away and the total step count - 65 is an equal multiple of the grid
        # height/width).
        n = (steps - edge) // garden.cols

        # With all the values now known, calculate the number number of
        # reachable plots after traversing n grid widths past the edge of the
        # initial grid.
        return (a * n**2) + (b * n) + c


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day21(example=True)
    aoc.validate(aoc.part1(), 16)
    # Run against actual data
    aoc = AOC2023Day21(example=False)
    aoc.run()
