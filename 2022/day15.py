#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/15
'''
from __future__ import annotations
import functools
import itertools
import re
from collections.abc import Iterator

# Local imports
from aoc2022 import AOC2022

# Typing shortcuts
Coordinate = tuple[int, int]


# NOTE: I didn't end up using this class for anything (changed approach) but
# I'm keeping the code in case it's useful for something in the future :)
class Line:
    '''
    Represents a line, given two coordinates
    '''
    def __init__(
        self,
        coord1: Coordinate,
        coord2: Coordinate,
    ) -> None:
        '''
        Compute the slope and x/y-intercepts
        '''
        self.coord1 = coord1
        self.coord2 = coord2
        self.slope = (self.coord1[1] - self.coord2[1]) / (self.coord1[0] - self.coord2[0])
        self.y_int = self.coord1[1] - (self.slope * self.coord1[0])
        self.x_int = -self.y_int / self.slope

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Line(coord1={self.coord1!r}, coord2={self.coord2!r})'

    def __str__(self) -> str:
        '''
        Return line equation in slope/intercept format
        '''
        slope = int(self.slope) if self.slope == int(self.slope) else self.slope
        y_int = int(self.y_int) if self.y_int == int(self.y_int) else self.y_int

        if abs(slope) == 1:
            slope = str(slope)[:-1]

        ret = f'y = {slope}x'
        if self.y_int < 0:
            ret += f' - {abs(y_int)}'
        elif self.y_int > 0:
            ret += f' + {abs(y_int)}'
        return ret

    def __eq__(self, other) -> bool:
        '''
        Define == operator
        '''
        return self.slope == other.slope and self.y_int == other.y_int

    def intersection(self, other: Line) -> Coordinate:
        '''
        Return intersection of this line and another line
        '''
        try:
            col = (other.y_int - self.y_int) / (self.slope - other.slope)
        except ZeroDivisionError as exc:
            raise ValueError('Lines do not intersect') from exc

        row = (self.slope * col) + self.y_int

        if col == int(col):
            col = int(col)
        if row == int(row):
            row = int(row)

        return (col, row)


class Sensor:
    '''
    A single sensor and associated functiosn
    '''
    def __init__(
        self,
        coord: Coordinate,
        beacon: Coordinate,
    ) -> None:
        '''
        Initialize the object
        '''
        self.coord = coord
        self.beacon = beacon
        self.radius = self.distance(self.beacon)

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Sensor(coord={self.coord!r}, beacon={self.beacon!r}, radius={self.radius!r})'

    @property
    def col(self):
        '''
        Convenince attribute to return the x position
        '''
        return self.coord[0]

    @property
    def row(self):
        '''
        Convenince attribute to return the y position
        '''
        return self.coord[1]

    @functools.cached_property
    def frontier(self) -> list[Coordinate]:
        '''
        Returns a sequence of coordinates that are a distance of radius + 1
        from the Sensor's coordinates
        '''
        return list(
            itertools.chain(
                *(
                    zip(
                        range(
                            self.col,
                            (self.col + self.radius + 2) * x_sign,
                            x_sign
                        ),
                        reversed(range(
                            self.row,
                            (self.row + self.radius + 2) * y_sign,
                            y_sign
                        )),
                    )
                    for x_sign, y_sign in itertools.product((1, -1), repeat=2)
                )
            )
        )

    def distance(
        self,
        other: Coordinate | Sensor,
    ) -> int:
        '''
        Calculates the distance from another coordinate (or Sensor)
        '''
        try:
            coord = other.coord
        except AttributeError:
            coord = other

        return abs(self.coord[0] - coord[0]) + abs(self.coord[1] - coord[1])

    def visible(
        self,
        coord: Coordinate,
    ) -> int:
        '''
        Calculates the distance from another coordinate (or Sensor)
        '''
        return self.distance(coord) <= self.radius

    def excluded(
        self,
        row: int | None,
    ) -> Iterator[Coordinate]:
        '''
        Return a sequence of points known to be beacon-free
        '''
        excluded_range = self.radius

        for row_offset in range(-excluded_range, excluded_range + 1):
            scan_row = self.row + row_offset
            if row is None or row == scan_row:
                spread = excluded_range - abs(row_offset)
                for scan_col in range(
                    self.col - spread,
                    self.col + spread + 1,
                ):
                    coord = (scan_col, scan_row)
                    if coord != self.beacon:
                        yield coord


class AOC2022Day15(AOC2022):
    '''
    Day 15 of Advent of Code 2022
    '''
    day = 15

    def __init__(self, example: bool = False) -> None:
        '''
        Load the cleaning assignment pairs into tuples of sets of ints
        '''
        super().__init__(example=example)

        sensors = []
        sensor_re = re.compile(
            r'^Sensor at x=(-?\d+), y=(-?\d+): '
            r'closest beacon is at x=(-?\d+), y=(-?\d+)$'
        )

        with self.input.open() as fh:
            for line in fh:
                parsed = sensor_re.match(line.rstrip())
                sensors.append(
                    Sensor(
                        (int(parsed.group(1)), int(parsed.group(2))),
                        (int(parsed.group(3)), int(parsed.group(4))),
                    )
                )
        self.sensors = tuple(sensors)

    def part1(self) -> int:
        '''
        Return a count of excluded coordinates on a specific row
        '''
        row = 10 if self.example else 2_000_000
        coords = set()

        for sensor in self.sensors:
            if not (sensor.row - sensor.radius) <= row <= (sensor.row + sensor.radius):
                # Don't compute excluded coords if this sensor cannot see
                # anything on the specified row
                continue
            coords.update(sensor.excluded(row=row))

        return len(coords)

    def part2(self) -> int:
        '''
        Compute the tuning frequency
        '''
        search_min = 0
        search_max = 20 if self.example else 4_000_000

        for sensor1 in self.sensors:
            for coord in sensor1.frontier:
                if not (
                    search_min <= coord[0] <= search_max and
                    search_min <= coord[1] <= search_max
                ):
                    continue
                if not any(sensor2.visible(coord) for sensor2 in self.sensors):
                    return (coord[0] * 4_000_000) + coord[1]

        raise RuntimeError('Failed to find beacon!')


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day15(example=True)
    aoc.validate(aoc.part1(), 26)
    aoc.validate(aoc.part2(), 56000011)
    # Run against actual data
    aoc = AOC2022Day15(example=False)
    aoc.run()
