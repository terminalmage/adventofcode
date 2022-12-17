#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/15

--- Day 15: Beacon Exclusion Zone ---

You feel the ground rumble again as the distress signal leads you to a large
network of subterranean tunnels. You don't have time to search them all, but
you don't need to: your pack contains a set of deployable sensors that you
imagine were originally built to locate lost Elves.

The sensors aren't very powerful, but that's okay; your handheld device
indicates that you're close enough to the source of the distress signal to use
them. You pull the emergency sensor system out of your pack, hit the big button
on top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches
itself to a hard surface and begins monitoring for the nearest signal source
beacon. Sensors and beacons always exist at integer coordinates. Each sensor
knows its own position and can determine the position of a beacon precisely;
however, sensors can only lock on to the one beacon closest to the sensor as
measured by the Manhattan distance. (There is never a tie where two beacons are
the same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest
beacons (your puzzle input). For example:

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

So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For the
sensor at 9,16, the closest beacon to it is at 10,16.

Drawing sensors as S and beacons as B, the above arrangement of sensors and
beacons looks like this:

               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

This isn't necessarily a comprehensive map of all beacons in the area, though.
Because each sensor only identifies its closest beacon, if a sensor detects a
beacon, you know there are no other beacons that close or closer to that
sensor. There could still be beacons that just happen to not be the closest
beacon to any sensor. Consider the sensor at 8,7:

               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########*...........
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

This sensor's closest beacon is at 2,10, and so you know there are no beacons
that close or closer (in any positions marked #).

None of the detected beacons seem to be producing the distress signal, so
you'll need to work out where the distress beacon is by working out where it
isn't. For now, keep things simple by counting the positions where a beacon
cannot possibly be along just a single row.

So, suppose you have an arrangement of beacons and sensors like in the example
above and, just in the row where y=10, you'd like to count the number of
positions a beacon cannot possibly exist. The coverage from all sensors near
that row looks like this:

                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.

In this example, in the row where y=10, there are 26 positions where a beacon
cannot be present.

Consult the report from the sensors you just deployed. In the row where
y=2000000, how many positions cannot contain a beacon?

--- Part Two ---

Your handheld device indicates that the distress signal is coming from a beacon
nearby. The distress beacon is not detected by any sensor, but the distress
beacon must have x and y coordinates each no lower than 0 and no larger than
4000000.

To isolate the distress beacon's signal, you need to determine its tuning
frequency, which can be found by multiplying its x coordinate by 4000000 and
then adding its y coordinate.

In the example above, the search space is smaller: instead, the x and y
coordinates can each be at most 20. With this reduced search area, there is
only a single position that could have a beacon: x=14, y=11. The tuning
frequency for this distress beacon is 56000011.

Find the only possible position for the distress beacon. What is its tuning
frequency?
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
    aoc = AOC2022Day15(example=False)
    print(f'Answer 1: {aoc.part1()}')
    print(f'Answer 2: {aoc.part2()}')
