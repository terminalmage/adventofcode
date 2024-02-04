#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/15
'''
from __future__ import annotations
import functools
import itertools
import re
import textwrap
from collections.abc import Iterator

# Local imports
from aoc import AOC, XY


# NOTE: I didn't end up using this class for anything (changed approach) but
# I'm keeping the code in case it's useful for something in the future :)
class Line:
    '''
    Represents a line, given two coordinates
    '''
    def __init__(
        self,
        coord1: XY,
        coord2: XY,
    ) -> None:
        '''
        Compute the slope and x/y-intercepts
        '''
        self.coord1: XY = coord1
        self.coord2: XY = coord2
        self.slope: float = (self.coord1[1] - self.coord2[1]) / (self.coord1[0] - self.coord2[0])
        self.y_int: int = self.coord1[1] - (self.slope * self.coord1[0])
        self.x_int: int = -self.y_int / self.slope

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Line(coord1={self.coord1!r}, coord2={self.coord2!r})'

    def __str__(self) -> str:
        '''
        Return line equation in slope/intercept format
        '''
        slope: int = int(self.slope) if self.slope == int(self.slope) else self.slope
        y_int: int = int(self.y_int) if self.y_int == int(self.y_int) else self.y_int

        if abs(slope) == 1:
            slope: str = str(slope)[:-1]

        ret: str = f'y = {slope}x'
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

    def intersection(self, other: Line) -> XY:
        '''
        Return intersection of this line and another line
        '''
        try:
            col: float = (other.y_int - self.y_int) / (self.slope - other.slope)
        except ZeroDivisionError as exc:
            raise ValueError('Lines do not intersect') from exc

        row: float = (self.slope * col) + self.y_int

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
        coord: XY,
        beacon: XY,
    ) -> None:
        '''
        Initialize the object
        '''
        self.coord: XY = coord
        self.beacon: XY = beacon
        self.radius: int = self.distance(self.beacon)

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
    def frontier(self) -> list[XY]:
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
        other: XY | Sensor,
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
        coord: XY,
    ) -> int:
        '''
        Calculates the distance from another coordinate (or Sensor)
        '''
        return self.distance(coord) <= self.radius

    def excluded(
        self,
        row: int | None,
    ) -> Iterator[XY]:
        '''
        Return a sequence of points known to be beacon-free
        '''
        excluded_range: int = self.radius

        row_offset: int
        for row_offset in range(-excluded_range, excluded_range + 1):
            scan_row: int = self.row + row_offset
            if row is None or row == scan_row:
                spread: int = excluded_range - abs(row_offset)
                scan_col: int
                for scan_col in range(
                    self.col - spread,
                    self.col + spread + 1,
                ):
                    coord: XY = (scan_col, scan_row)
                    if coord != self.beacon:
                        yield coord


class AOC2022Day15(AOC):
    '''
    Day 15 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        Sensor at x=9, y=16: closest beacon is at x=10, y=16
        Sensor at x=13, y=2: closest beacon is at x=15, y=3
        Sensor at x=12, y=14: closest beacon is at x=10, y=16
        Sensor at x=10, y=20: closest beacon is at x=10, y=16
        Sensor at x=14, y=17: closest beacon is at x=10, y=16
        Sensor at x=8, y=7: closest beacon is at x=2, y=10
        Sensor at x=2, y=0: closest beacon is at x=2, y=10
        Sensor at x=0, y=11: closest beacon is at x=2, y=10
        Sensor at x=20, y=14: closest beacon is at x=25, y=17
        Sensor at x=17, y=20: closest beacon is at x=21, y=22
        Sensor at x=16, y=7: closest beacon is at x=15, y=3
        Sensor at x=14, y=3: closest beacon is at x=15, y=3
        Sensor at x=20, y=1: closest beacon is at x=15, y=3
        '''
    )

    validate_part1: int = 26
    validate_part2: int = 56000011

    # Set by post_init
    sensors = None

    def post_init(self) -> None:
        '''
        Load the cleaning assignment pairs into tuples of sets of ints
        '''
        sensors: list[Sensor] = []
        sensor_re: re.Pattern = re.compile(
            r'^Sensor at x=(-?\d+), y=(-?\d+): '
            r'closest beacon is at x=(-?\d+), y=(-?\d+)$'
        )

        for line in self.input.splitlines():
            parsed: re.Match = sensor_re.match(line)
            sensors.append(
                Sensor(
                    (int(parsed.group(1)), int(parsed.group(2))),
                    (int(parsed.group(3)), int(parsed.group(4))),
                )
            )
        self.sensors: tuple[Sensor, ...] = tuple(sensors)

    def part1(self) -> int:
        '''
        Return a count of excluded coordinates on a specific row
        '''
        row: int = 10 if self.example else 2_000_000
        coords: set[XY] = set()

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
        search_min: int = 0
        search_max: int = 20 if self.example else 4_000_000

        sensor1: Sensor
        sensor2: Sensor
        coord: XY
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
    aoc = AOC2022Day15()
    aoc.run()
