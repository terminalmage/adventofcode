#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/10
'''
from __future__ import annotations
import math
import re
import textwrap
from collections.abc import Generator
from dataclasses import dataclass

# Local imports
from aoc import AOC, XY, XYMixin, directions, opposite_directions

OPPOSITE: dict[int, XY] = {
    directions._fields[n][0]: opposite_directions._fields[n][0]
    for n in range(len(directions))
}

SHAPES: frozenset[str] = frozenset('|-LJ7F')


@dataclass
class PipeCoord:
    '''
    Represents a coordinate and its neighbors
    '''
    value: XY

    def __getitem__(self, name: str) -> PipeCoord:
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

    def __eq__(self, other: PipeCoord) -> bool:
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
        self.sketch: str = sketch
        self.segments: dict[XY, PipeSegment] = {}
        self.start: PipeSegment | None = None

        lines: list[str] = self.sketch.splitlines()
        self.num_rows: int = len(lines)
        self.num_cols: int = len(lines[0])

        row_num: int
        col_num: int
        row: str
        shape: str
        for row_num, row in enumerate(lines):
            for col_num, shape in enumerate(row):
                if shape in SHAPES or shape == 'S':
                    coord: PipeCoord = PipeCoord((row_num, col_num))
                    self.segments[coord.as_tuple] = PipeSegment(
                        coord=coord,
                        shape=shape,
                        parent=self,
                    )
                    if shape == 'S':
                        self.start: PipeSegment = self.segments[coord.as_tuple]

        if self.start is None:
            raise ValueError('No start point detected in pipe map')

        # Discover exits for start pipe
        direction: XY
        for direction in OPPOSITE:
            try:
                neighbor: PipeSegment = self.segments[self.start.coord[direction].as_tuple]
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
    def loop_segments(self) -> Generator[PipeSegment, None, None]:
        '''
        Generator which yields a sequence of PipeSegment objects, starting at
        the start point, and ending when the start has been reached again.
        '''
        location: XY = self.start
        direction: str = self.start.exits[0]

        while True:
            yield location

            # Find next PipeSegment based on the current direction
            next_coord: XY = location.coord[direction]
            next_segment: PipeSegment = self.segments[next_coord.as_tuple]

            if next_segment == self.start:
                # We've reached the beginning of the loop again
                break

            # Update location for next loop iteration
            location: PipeSegment = next_segment

            # Find the new direction. Start by getting the direction from which
            # we entered the new segment, which will be the opposite of the
            # direction which we are currently pointed.
            entry: str = OPPOSITE[direction]
            # Get the string index of the new direction
            next_direction_index: int = (next_segment.exits.index(entry) + 1) % 2
            # Update direction for next loop iteration
            direction: str = next_segment.exits[next_direction_index]

    @property
    def inside_loop(self) -> Generator[tuple[int], None, None]:
        '''
        Use regexes to implement even-odd method for detecting whether a point
        is inside a polygon.
        '''
        loop_coords: frozenset[XY] = frozenset(
            segment.coord.as_tuple for segment in self.loop_segments
        )
        border_re: re.Pattern = re.compile(r'\||F-*J|L-*7')
        row_num: int
        col_num: int
        row: str
        col: str
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

    def __eq__(self, other: PipeSegment) -> bool:
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
    example_data_part1: str = textwrap.dedent(
        '''
        ..F7.
        .FJ|.
        SJ.L7
        |F--J
        LJ...
        '''
    )
    example_data_part2: str = textwrap.dedent(
        '''
        FF7FSF7F7F7F7F7F---7
        L|LJ||||||||||||F--J
        FL-7LJLJ||||||LJL-77
        F--JF--7||LJLJ7F7FJ-
        L---JF-JLJ.||-FJLJJ7
        |F|F-JF---7F7-L7L|7|
        |FFJF7L7F-JF7|JL---7
        7-L-JL7||F7|L7F-7F7|
        L.L7LFJ|||||FJL7||LJ
        L7JLJL-JLJLJL--JLJ.L
        '''
    )

    validate_part1: int = 8
    validate_part2: int = 10

    def part1(self) -> int:
        '''
        Return the furthest length from the start point. This is calculated as
        the ceiling of the number of segments in the pipe divided by two. For
        example, if there are 15 segments in the loop, the furthest length will
        be ceil(7.5), or 8. If there are 200 segments in the loop, the furthest
        length will be ceil(100), or 100.
        '''
        pipe_map: PipeMap = PipeMap(self.input_part1)
        return math.ceil(len(list(pipe_map.loop_segments)) / 2)

    def part2(self) -> int:
        '''
        Return the number of tiles that are within the loop
        '''
        pipe_map: PipeMap = PipeMap(self.input_part2)
        return len(list(pipe_map.inside_loop))

    def part2_alt(self) -> int:
        '''
        Return the number of tiles that are within the loop

        This is an alternate solution using Pick's Theorem and the Shoelace
        Formula. For a more detailed explanation of this, see the docstring for
        the "solve" method in 2023 Day 18.
        '''
        pipe_map: PipeMap = PipeMap(self.input_part2)
        bounds = [p.coord.as_tuple for p in pipe_map.loop_segments]
        A = self.shoelace(bounds)
        b = self.perimeter(bounds)
        i = A - (b / 2) + 1
        return int(i)


if __name__ == '__main__':
    aoc = AOC2023Day10()
    aoc.run()
