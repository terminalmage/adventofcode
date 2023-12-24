#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/18
'''
# Local imports
from aoc import AOC, XYMixin, XY, directions


class AOC2023Day18(AOC, XYMixin):
    '''
    Day 18 of Advent of Code 2023
    '''
    day = 18

    def solve(self, bounds: list[XY]) -> int:
        '''
        Since the excavator only moves in 2 dimensions, we can disregard the
        3rd dimension and work in two dimensions. The puzzle solution is
        equivalent to the number of 1 cubic meter blocks that were excavated.
        If we imagine the excavator as drawing an irregular polygon, what is
        being requested here is the line traced by the excavator (i.e. the
        perimeter of the blocks that were excavated) plus the blocks inside of
        that line.

        Fortunately, both of these items are components of Pick's Theorem:

            https://en.wikipedia.org/wiki/Pick%27s_theorem

        Here is the formula:

            A = i + b/2 - 1

        The solution to this puzzle is therefore equal to i + b.

        A is the area, i is the number of integer coordinate points internal to
        the polygon, and b is the perimeter of the polygon.

        The only parameter we have access to at the start is b, which can be
        calculated by summing the lengths between each coordinate. So we need
        to calculate i. Solving for i, we can re-arrange the formula as
        follows:

            A = i + b/2 - 1
            i + b/2 - 1 = A     # Flip formula to put i on left
            i - 1 = A - b/2     # Move b/2 to right via subtraction
            i = A - b/2 + 1     # Move -1 to right via addition

        So, to calculate i, we need the area A, which we don't yet have.
        Fortunately, we can get the area by other means, using the Shoelace
        Formula:

            https://en.wikipedia.org/wiki/Shoelace_formula

        Once we have the area, we have everything we need to calculate i, and
        we can add this to our perimeter (b) to get the answer.
        '''
        # These helper functions come from the XYMixin
        A = self.shoelace(bounds)
        b = self.perimeter(bounds)
        i = A - (b / 2) + 1
        # Because of the way the puzzle is worded, we know that the answer will
        # be a whole number, so convert to an int before returning.
        return int(i + b)

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
