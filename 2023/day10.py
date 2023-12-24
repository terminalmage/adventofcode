#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/10
'''
import math
import re
from collections.abc import Generator
from dataclasses import dataclass
from typing import Self

# Local imports
from aoc import AOC, XY, XYMixin, directions, opposite_directions

OPPOSITE = {
    directions._fields[n][0]: opposite_directions._fields[n][0]
    for n in range(len(directions))
}

SHAPES = frozenset('|-LJ7F')


@dataclass
class PipeCoord:
    '''
    Represents a coordinate and its neighbors
    '''
    value: XY

    def __getitem__(self, name: str) -> Self:
        '''
        Handle directional movement
        '''
        match name:
            case 'N':
                delta = directions.NORTH
            case 'S':
                delta = directions.SOUTH
            case 'W':
                delta = directions.WEST
            case 'E':
                delta = directions.EAST
            case _:
                raise ValueError(f'Invalid direction {name!r}')

        return PipeCoord(tuple(a + b for a, b in zip(self.value, delta)))

    def __eq__(self, other: Self) -> bool:
        '''
        Define == operator
        '''
        if not isinstance(other, PipeCoord):
            return False
        return self.value == other.value

    def __repr__(self) -> str:
        '''
        Define repr() output for object
        '''
        return f'PipeCoord({self.value})'

    @property
    def as_tuple(self) -> tuple[int]:
        '''
        Return the row and column as a tuple
        '''
        return self.value


class PipeMap:
    '''
    Represents the entire grid of PipeSegments
    '''
    def __init__(self, sketch: str) -> None:
        '''
        Read in the map data and create PipeSegment
        '''
        self.sketch = sketch
        self.segments = {}
        self.start = None

        lines = self.sketch.splitlines()
        self.num_rows = len(lines)
        self.num_cols = len(lines[0])

        for row_num, row in enumerate(lines):
            for col_num, shape in enumerate(row):
                if shape in SHAPES or shape == 'S':
                    coord = PipeCoord((row_num, col_num))
                    self.segments[coord.as_tuple] = PipeSegment(
                        coord=coord,
                        shape=shape,
                        parent=self,
                    )
                    if shape == 'S':
                        self.start = self.segments[coord.as_tuple]

        if self.start is None:
            raise ValueError('No start point detected in pipe map')

        # Discover exits for start pipe
        for direction in OPPOSITE:
            try:
                neighbor = self.segments[self.start.coord[direction].as_tuple]
            except KeyError:
                continue
            else:
                # Make sure that the neighboring PipeSegment connects directly
                # to the start point. This prevents a non-connecting (but
                # adjacent) PipeSegment from being erroneously identified as an
                # exit.
                if OPPOSITE[direction] in neighbor.exits:
                    self.start.exits += direction

        if len(self.start.exits) != 2:
            raise ValueError(
                f'{len(self.start.exits)} exits found for start point '
                f'(expected 2)'
            )

        # Now that we know the exits for the start point, set the shape for
        # this PipeSegment. This will be necessary for boundary detection, to
        # determine whether or not a given tile is within the loop.
        match sorted(self.start.exits):
            case ['N', 'S']:
                self.start.shape = '|'
            case ['E', 'W']:
                self.start.shape = '-'
            case ['E', 'N']:
                self.start.shape = 'L'
            case ['N', 'W']:
                self.start.shape = 'J'
            case ['S', 'W']:
                self.start.shape = '7'
            case ['E', 'S']:
                self.start.shape = 'F'
            case _:
                raise ValueError('Failed to detect shape of start point')

    @property
    def loop_segments(self) -> Generator['PipeSegment', None, None]:
        '''
        Generator which yields a sequence of PipeSegment objects, starting at
        the start point, and ending when the start has been reached again.
        '''
        location = self.start
        direction = self.start.exits[0]

        while True:
            yield location

            # Find next PipeSegment based on the current direction
            next_coord = location.coord[direction]
            next_segment = self.segments[next_coord.as_tuple]

            if next_segment == self.start:
                # We've reached the beginning of the loop again
                break

            # Update location for next loop iteration
            location = next_segment

            # Find the new direction. Start by getting the direction from which
            # we entered the new segment, which will be the opposite of the
            # direction which we are currently pointed.
            entry = OPPOSITE[direction]
            # Get the string index of the new direction
            next_direction_index = (next_segment.exits.index(entry) + 1) % 2
            # Update direction for next loop iteration
            direction = next_segment.exits[next_direction_index]

    @property
    def inside_loop(self) -> Generator[tuple[int], None, None]:
        '''
        Use regexes to implement even-odd method for detecting whether a point
        is inside a polygon.
        '''
        loop_coords = frozenset(
            segment.coord.as_tuple for segment in self.loop_segments
        )
        border_re = re.compile(r'\||F-*J|L-*7')
        for row_num, row in enumerate(self.sketch.splitlines()):
            # Rewrite the line, replacing all non-loop columns with dots. With
            # non-loop pipe segments removed, the regex defined above will
            # accurately match loop boundaries.
            row = ''.join(
                '.' if (row_num, col_num) not in loop_coords
                else self.segments[(row_num, col_num)].shape
                for col_num in range(len(row))
            )
            for col_num, col in enumerate(row):
                if (
                    col == '.'
                    and len(border_re.findall(row[:col_num])) % 2
                ):
                    # Coordinate is not part of the loop itself, and there are
                    # an odd number of boundaries detected to the left of it.
                    # Therefore the coordinate is inside the loop.
                    yield (row_num, col_num)


class PipeSegment:
    '''
    Represents a segment of pipe
    '''
    def __init__(
        self,
        coord: PipeCoord,
        shape: str,
        parent: PipeMap,
    ) -> None:
        '''
        Initialize the object, defining the direction of the exits
        '''
        self.coord = coord
        self.shape = shape
        self.parent = parent

        match self.shape:
            case '|':
                self.exits = 'NS'
            case '-':
                self.exits = 'WE'
            case 'L':
                self.exits = 'NE'
            case 'J':
                self.exits = 'NW'
            case '7':
                self.exits = 'SW'
            case 'F':
                self.exits = 'SE'
            case 'S':
                self.exits = ''
            case _:
                raise ValueError(f'Invalid shape {shape!r}')

    def __eq__(self, other: 'PipeSegment') -> bool:
        '''
        Define == operator
        '''
        return self.coord == other.coord

    def __repr__(self) -> str:
        '''
        Define repr() output for object
        '''
        return f'PipeSegment(coord={self.coord}, shape={self.shape!r})'


class AOC2023Day10(AOC, XYMixin):
    '''
    Day 10 of Advent of Code 2023
    '''
    day = 10

    def part1(self) -> int:
        '''
        Return the furthest length from the start point. This is calculated as
        the ceiling of the number of segments in the pipe divided by two. For
        example, if there are 15 segments in the loop, the furthest length will
        be ceil(7.5), or 8. If there are 200 segments in the loop, the furthest
        length will be ceil(100), or 100.
        '''
        pipe_map = PipeMap(self.get_input(part=1).read_text())
        return math.ceil(len(list(pipe_map.loop_segments)) / 2)

    def part2(self) -> int:
        '''
        Return the number of tiles that are within the loop
        '''
        pipe_map = PipeMap(self.get_input(part=2).read_text())
        return len(list(pipe_map.inside_loop))

    def part2_alt(self) -> int:
        '''
        Return the number of tiles that are within the loop

        This is an alternate solution using Pick's Theorem and the Shoelace
        Formula. For a more detailed explanation of this, see the docstring for
        the "solve" method in 2023 Day 18.
        '''
        pipe_map = PipeMap(self.get_input(part=2).read_text())
        bounds = [p.coord.as_tuple for p in pipe_map.loop_segments]
        A = self.shoelace(bounds)
        b = self.perimeter(bounds)
        i = A - (b / 2) + 1
        return int(i)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day10(example=True)
    aoc.validate(aoc.part1(), 8)
    aoc.validate(aoc.part2(), 10)
    # Run against actual data
    aoc = AOC2023Day10(example=False)
    aoc.run()
