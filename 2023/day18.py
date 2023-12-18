#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/18
'''
# Local imports
from aoc import (
    AOC,
    CoordinateMixin,
    Coordinate,
    directions,
)


class AOC2023Day18(AOC, CoordinateMixin):
    '''
    Day 18 of Advent of Code 2023
    '''
    day = 18

    def solve(self, bounds: list[Coordinate]) -> int:
        '''
        Since the excavator only moves in 2 dimensions, we can simply calculate
        the area inside the bounds, and then add 0.5 cubic meter for each point
        that forms the perimeter. This extra space is required because in this
        scenario the excavator digs out 1 cubic meter chunks, and imagining
        each coordinate as being in the center of the excavated area, half of
        the volume of each perimiter coordinate lies within the area that we
        will be calculating, and the other half lies outside.

        For the area, use the shoelace formula helper from the parent class.

        The extra space we need to add for the perimeter is equal to:

            (perimeter / 2) + 1

        Thus, the total volume is equal to:

            area + (perimeter / 2) + 1
        '''
        return self.shoelace(bounds) + (self.perimeter(bounds) // 2) + 1

    def part1(self) -> int:
        '''
        Solve for Part 1
        '''
        deltas = {
            'U': directions.NORTH,
            'D': directions.SOUTH,
            'L': directions.WEST,
            'R': directions.EAST,
        }

        row = col = 0
        bounds = [(row, col)]

        with self.input.open() as fh:
            for line in fh:
                direction, distance = line.split(None, 2)[:2]
                distance = int(distance)
                row, col = (
                    item + distance * delta
                    for item, delta in zip((row, col), deltas[direction])
                )
                bounds.append((row, col))

        return self.solve(bounds)

    def part2(self) -> int:
        '''
        Solve for Part 2
        '''
        deltas = {
            '0': directions.EAST,
            '1': directions.SOUTH,
            '2': directions.WEST,
            '3': directions.NORTH,
        }

        row = col = 0
        bounds = [(row, col)]

        with self.input.open() as fh:
            for line in fh:
                color_hex = line.split()[-1][2:8]
                distance = int(color_hex[:5], 16)
                direction = color_hex[-1]
                row, col = (
                    item + distance * delta
                    for item, delta in zip((row, col), deltas[direction])
                )
                bounds.append((row, col))

        return self.solve(bounds)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day18(example=True)
    aoc.validate(aoc.part1(), 62)
    aoc.validate(aoc.part2(), 952408144115)
    # Run against actual data
    aoc = AOC2023Day18(example=False)
    aoc.run()
