#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/3
'''
import itertools
import math
import textwrap

# Local imports
from aoc import AOC, XY, XYMixin, TupleMixin, directions, ordinal_directions


class AOC2017Day3(AOC, XYMixin, TupleMixin):
    '''
    Day 3 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        1024
        '''
    )

    validate_part1: int = 31

    walk_order: tuple[XY] = (
        directions.NORTH,
        directions.WEST,
        directions.SOUTH,
        directions.EAST,
    )

    def post_init(self) -> None:
        '''
        Set the target value depending on whether or not we are running with
        the example data.
        '''
        self.target: int = int(self.input)

    def part1(self) -> int:
        '''
        Compute the Manhattan Distance between the number at the target
        position and the starting position (0, 0).
        '''
        # Find the highest square of an odd number, that is still lower than
        # the target position.
        sqrt: int = int(math.sqrt(self.target))
        if not sqrt % 2:
            # Make sure the square root is actually odd
            sqrt -= 1

        square: int = sqrt ** 2

        # Account for the (literal) corner case where the target is itself a
        # square of an odd number. If that's the case, we don't need to
        # calculate the delta.
        if square == self.target:
            new_pos: XY = 2 * (((sqrt - 1) // 2),)
        else:
            # We're not going to manually walk around the spiral. We know
            # because of the math we did above that the number is within this
            # next spiral layer. We also know how far away from that target we
            # are. We can therefore just sum up all the coordinate deltas that
            # would be traversed in that many moves. We now have a single delta
            # that will get us to the correct position. We just need a starting
            # point from which to apply that delta. If you think about what the
            # process would be like, were we to be counting manually, it would
            # be ideal if we could count up, left, down, and then right. So for
            # that first move upward to be one right of the end of the previous
            # spiral layer, the correct place to start from is the position
            # below the first number in the new spiral layer. For example,
            # heres the spiral from the puzzle:
            #
            # 17  16  15  14  13
            # 18   5   4   3  12
            # 19   6   1   2  11
            # 20   7   8   9  10
            # 21  22  23---> ...
            #
            # Say we want to know the position of 16, and it wasn't both
            # trivial and already in the example. We would have calculated the
            # nearest odd-square as 9. We know we need to count up seven to get
            # there. The correct starting point is the point diagonally down
            # and to the right of the 9. From there we just need to know the
            # length that we would move, in each direction for this spiral
            # layer. Well, we know that the next layer ends in 5² (25), so
            # subtracting the 9 leaves 16, divided by 4 sides equals 4 steps in
            # each direction to get to the end of the new spiral layer. So,
            # since we want to find the location of 16, and 16 is 7 away, it
            # will be the equivalent of the sum of 4 up moves and 3 left moves.
            # If we wanted to know the location of 23 (14 away from 9), it
            # would be the same as 4 up moves, plus 4 left moves, plus 4 down
            # moves, plus 2 right moves.
            sides: int
            rem: int
            sides, rem = divmod(self.target - square, sqrt + 1)
            side_length: int = (((sqrt + 2) ** 2) - square) // 4

            # The delta we will be moving to "walk" to the target number
            delta: XY = (0, 0)
            # Incrememnt the delta for each full side of the spiral.
            # NOTE: The tuple_* functions here come from the TupleMixin
            # imported from my aoc lib.
            for i in range(sides):
                delta = self.tuple_add(
                    delta,
                    self.tuple_multiply_all(self.walk_order[i], side_length),
                )

            if rem:
                # self.walk_order[sides] will be the index of the direction we
                # need to move for the remaining steps.
                delta = self.tuple_add(
                    delta,
                    self.tuple_multiply_all(self.walk_order[sides], rem),
                )

            # The X and Y offset from (0, 0) of a given odd-square is the
            # square root of that square minus 1, divided by 2. So the start
            # point from which we will be applying the delta is the next
            # level's offset, which would be the square root + 2 - 1 (or just +
            # 1), divided by 2. Since the x and y offset is the same, use tuple
            # multiplication to get a 2-tuple with the same x and y value.
            start_point: XY = 2 * (((sqrt + 1) // 2),)

            new_pos: XY = self.tuple_add(start_point, delta)

        # Return the distance to the new position
        return self.distance((0, 0), new_pos)

    def part2(self) -> int:
        '''
        Implement the spiral integer sequence from Part 2 and return the first
        integer greater than the target number
        '''
        start: XY = (0, 0)
        spiral: dict[XY, int] = {start: 1}

        def sum_adjacent(coord: XY) -> int:
            '''
            Return the sum of all adjacent tiles which have already been
            defined in the spiral.
            '''
            return sum(
                spiral.get(
                    self.tuple_add(coord, delta),
                    0
                ) for delta in itertools.chain.from_iterable(
                    (directions, ordinal_directions)
                )
            )

        position: XY = start
        side_length: int
        for side_length in itertools.count(2, 2):
            # Move pointer down and to the right to start the new spiral layer
            position = self.tuple_add(position, (1, 1))
            # Count side_length times for each direction in the walk_order
            delta: XY
            for delta in itertools.chain.from_iterable(
                ((d,) * side_length for d in self.walk_order)
            ):
                position = self.tuple_add(position, delta)
                # Now I need a function to check all directions and ordinal
                # directions for values, and return the sum. That value is what
                # we'll put into this position. Then all we need is a check to
                # see if we've exceeded the target.
                spiral[position] = sum_adjacent(position)
                if spiral[position] > self.target:
                    return spiral[position]


if __name__ == '__main__':
    aoc = AOC2017Day3()
    aoc.run()
