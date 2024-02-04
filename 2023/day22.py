#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/22
'''
import re
import textwrap
from collections import deque

# Local imports
from aoc import AOC, XYZ


class Brick:
    '''
    Represents a single brick
    '''
    def __init__(self, begin: XYZ, end: XYZ) -> int:
        '''
        Initialize object
        '''
        self.begin: XYZ = begin
        self.end: XYZ = end
        self.children: set[Brick] = set()
        self.parents: set[Brick] = set()

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Brick(begin={self.begin!r}, end={self.end!r})'

    @property
    def coordinates(self) -> set[XYZ]:
        '''
        Return all coordinates that belong to this brick
        '''
        return {
            (x, y, z)
            for x in range(self.begin[0], self.end[0] + 1)
            for y in range(self.begin[1], self.end[1] + 1)
            for z in range(self.begin[2], self.end[2] + 1)
        }

    @property
    def out_of_bounds(self) -> bool:
        '''
        Assuming the z-value of 0 being occupied by the bottom of the Chasm, a
        Brick is out-of-bounds if any of its coordinates' z-values are less
        than 1.
        '''
        return any(coord[-1] < 1 for coord in (self.begin, self.end))

    def copy(self) -> 'Brick':
        '''
        Return a new Brick with the same coordinates
        '''
        return Brick(self.begin, self.end)

    def move_down(self) -> 'Brick':
        '''
        Move the Brick one z-value down. Returns itself.
        '''
        self.begin = (self.begin[0], self.begin[1], self.begin[2] - 1)
        self.end = (self.end[0], self.end[1], self.end[2] - 1)
        return self

    def move_up(self) -> 'Brick':
        '''
        Move the Brick one z-value up. Returns itself.
        '''
        self.begin = (self.begin[0], self.begin[1], self.begin[2] + 1)
        self.end = (self.end[0], self.end[1], self.end[2] + 1)
        return self


class Chasm:
    '''
    Object which manages a Brick object for each brick defined in the input
    '''
    def __init__(self, data: str) -> None:
        '''
        Load all the bricks from the puzzle input

        Key insights about the input:

        - For each Brick definition, there are 2 x,y,z coordinates representing
          opposite ends of each Brick.

        - The values for these coordinates are in order on a given line (i.e.
          the x/y/z-values for one coordinate are followed by x/y/z-values for
          the other coordinate), and are not contiguous (i.e. each integer is
          separated either by a comma or a tilde). This means that we can use a
          regex to detect all integers instead of using a multi-step process of
          string-splitting. The first three integers matching the regex will
          belong to one coordinate, and the remaining will belong to the other
          coordinate.

        - Some bricks lay horizontally (i.e. the z-values are the same on both
          ends).

        - For the bricks that lay vertically (i.e. the z-values are different),
          the lower z-value is _always_ found in the first coordinate (i.e. the
          3rd digit detected on each line).

        - If two bricks share the same minimum (i.e. first) z-value, then they
          can't possibly collide with one another as they fall (i.e. they are
          across from/adjacent to one another and their lowest points are
          equal). In other words, the x/y-values don't matter for the purposes
          of drop order, only the z-value, and bricks which share a minimum
          z-value can be dropped in any order.

        Using these insights, we can detect each line's integers, and then sort
        the lines by the 3rd integer on each line. This will give us a sequence
        of bricks in the exact order needed to simulate the initial drop
        defined in the puzzle (i.e. lowest bricks first, highest bricks last).
        '''
        self.bricks: tuple[Brick, ...] = tuple(
            Brick(begin=(x1, y1, z1), end=(x2, y2, z2))
            for x1, y1, z1, x2, y2, z2 in sorted(
                (
                    tuple(int(x) for x in re.findall(r'\d+', line))
                    for line in data.splitlines()
                ),
                key=lambda brick_xyzxyz: brick_xyzxyz[2]
            )
        )

        # In the loop below, when each Brick comes to a rest, this dict will be
        # used to map its coordinates to the Brick instance, so that the bricks
        # in subsequent loop iterations know exactly which brick(s) they are
        # colliding with.
        new_locations: dict[XYZ, Brick] = {}

        # Simulate dropping bricks, detecting which bricks would collide with
        # which other bricks. If a brick collides with another brick, it is a
        # "child" of that brick.
        for brick in self.bricks:
            # First, create a copy of the Brick instance so that we don't
            # modify the one from self.bricks.
            new_brick: Brick = brick.copy()
            # Initialize collisions to account for possible case where the
            # brick starts out resting on the bottom of the Chasm (and thus the
            # while block is never entered.
            collisions: set[Brick] = set()
            # Drop the copied brick one z-value at a time until the bottom is
            # reached (or a collision is detected).
            while not new_brick.move_down().out_of_bounds:
                # Construct a set of the Brick instances with which this
                # falling brick has collided.
                collisions: set[Brick] = {
                    new_locations[coord] for coord in new_brick.coordinates
                    if coord in new_locations
                }
                if collisions:
                    # Collision detected
                    break

            # The brick either reached the bottom or collided with another
            # brick. Either way, it can't stay in this location and needs to
            # move back up by one.
            new_brick.move_up()

            # Keep track of the new location of the brick, mapping each of its
            # coordinates to the Brick object itself. This enables future loop
            # iterations to know which Brick(s) they collide with.
            new_locations.update(
                {coord: brick for coord in new_brick.coordinates}
            )

            # Update the parent/children relationships for the affected bricks.
            # The current brick will be a "child" of the bricks that it
            # collided with, and the collided-with bricks will be "parents" of
            # this brick.
            for collided_with in collisions:
                collided_with.children.add(brick)
                brick.parents.add(collided_with)

    @property
    def safe(self) -> set[Brick]:
        '''
        Return a set of bricks that can be safely disintegrated (that is,
        removing them would not cause any other bricks to fall).

        A brick is "safe" if it has no children, or if all of its children have
        more than one parent (i.e. removing that brick would leave at least one
        remaining to support each of its children).
        '''
        return {
            brick for brick in self.bricks
            if not brick.children or all(
                len(child.parents) > 1 for child in brick.children
            )
        }

    def supports(self, brick: Brick) -> set[Brick]:
        '''
        Return the bricks that this brick supports, both directly and
        indirectly. In other words, if this brick were removed, which others
        would fall?
        '''
        # Aggregates all children we've checked
        visited: set[Brick] = set()
        ret: set[Brick] = set()
        dq: deque[Brick] = deque([brick])

        # This loop simulates the chain reaction which would result from this
        # brick being removed. Each of the children of this brick will be
        # checked, and (along with the initial brick) aggregated into the
        # "visited" set. For a given child, if the set of visited bricks
        # contains all bricks that are parents of that child, then the child
        # would also fall as a result of removing the original brick.
        while dq:
            current_brick: Brick = dq.popleft()
            visited.add(current_brick)
            for child in current_brick.children:
                if not child.parents - visited:
                    # This child would fall
                    ret.add(child)
                    # Check all of this brick's children as well, to see if
                    # they would also fall
                    dq.append(child)

        return ret


class AOC2023Day22(AOC):
    '''
    Day 22 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        1,0,1~1,2,1
        0,0,2~2,0,2
        0,2,3~2,2,3
        0,0,4~0,2,4
        2,0,5~2,2,5
        0,1,6~2,1,6
        1,1,8~1,1,9
        '''
    )

    validate_part1: int = 5
    validate_part2: int = 7

    # Set by post_init
    chasm = None

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.chasm: Chasm = Chasm(self.input)

    def part1(self) -> int:
        '''
        Return the number of bricks which are safe to disintegrate (i.e. those
        that, if removed, would not cause any other bricks to fall).
        '''
        return len(self.chasm.safe)

    def part2(self) -> int:
        '''
        Calculate the number of bricks that would fall as a result of each
        brick being disintegrated, and return the sum of these counts.
        '''
        return sum(
            len(self.chasm.supports(brick))
            for brick in self.chasm.bricks
        )


if __name__ == '__main__':
    aoc = AOC2023Day22()
    aoc.run()
