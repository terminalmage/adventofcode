#!/usr/bin/env python
"""
https://adventofcode.com/2018/day/17
"""
from __future__ import annotations
import re
import textwrap
from collections import Counter, deque
from dataclasses import dataclass
from typing import Literal

# Local imports
from aoc import AOC, Grid, XY

AT_REST: str = "~"
FLOWING: str = "|"
ROCK: str = "#"
EMPTY: str = "."

# Type hints
Tile = Literal[EMPTY, ROCK, FLOWING, AT_REST]


@dataclass
class Bounds:
    """
    Stores min/max values
    """
    min: int = int(1e9)
    max: int = 0


class Scan:
    """
    A single scan from the puzzle input
    """
    scan_re: re.Pattern = re.compile(r"^(x|y)=(\d+), .=(\d+)\.+(\d+)")

    def __init__(self, line: str):
        """
        Parse the scan line
        """
        scan: re.Match = self.scan_re.match(line)
        self.axis: Literal["x", "y"] = scan.group(1)
        self.point: int = int(scan.group(2))  # Point on the axis
        self.low: int = int(scan.group(3))
        self.high: int = int(scan.group(4))

    def __repr__(self) -> str:
        """
        Define repr() output
        """
        return (
            f"Scan(axis: {self.axis!r}, point: {self.point}, "
            f"low: {self.low}, high: {self.high})"
        )


class XSection(Grid):
    """
    Stores scan data in a grid and adds a solver method
    """
    def __init__(self, scan_data: str) -> None:
        """
        Load the scans
        """
        self.x: Bounds = Bounds()
        self.y: Bounds = Bounds()

        scans: list[Scan] = [Scan(line) for line in scan_data.splitlines()]

        scan: str
        for scan in scans:
            axis: Bounds = getattr(self, scan.axis)
            other_axis: Bounds = getattr(self, "y" if scan.axis == "x" else "x")
            axis.min = min(axis.min, scan.point)
            axis.max = max(axis.max, scan.point)
            other_axis.min = min(other_axis.min, scan.low)
            other_axis.max = max(other_axis.max, scan.high)

        # Allow for overflow on each side of the leftmost/rightmost column
        self.x.min -= 1
        self.x.max += 1

        # With the bounds determined, build out an empty grid of the size that
        # we need for this puzzle
        grid_contents: list[list[Tile]] = [
            ['.'] * (self.x.max - self.x.min + 1)
            for _ in range(self.y.max + 1)
        ]

        # Draw in the rock chars using the scan data
        cur: int
        row: int
        col: int
        for scan in scans:
            for cur in range(scan.low, scan.high + 1):
                match scan.axis:
                    case "x":
                        col = scan.point - self.x.min
                        row = cur
                    case "y":
                        col = cur - self.x.min
                        row = scan.point
                grid_contents[row][col] = ROCK

        # Initialize the grid using the contents assembled above
        super().__init__(grid_contents)

        # We didn't make the grid start at column 0 because the majority of the
        # grid would be empty space, So, all columns in the grid are offset by
        # the value of the minimum bound of the x-axis. Therefore, the offset
        # source of the water can be calculated by substracting the minimum
        # bound of the x-axis. Note that though the type hint here is called
        # "XY", the Grid object contains a list of lists, so it is indexed as
        # (row, col) instead of (col, row)
        self.water_source: XY = (0, 500 - self.x.min)


class AOC2018Day17(AOC):
    """
    Day 17 of Advent of Code 2018
    """
    example_data: str = textwrap.dedent(
        """
        x=495, y=2..7
        y=7, x=495..501
        x=501, y=3..7
        x=498, y=2..4
        x=506, y=1..2
        x=498, y=10..13
        x=504, y=10..13
        y=13, x=498..504
        """
    )

    validate_part1: int = 57
    validate_part2: int = 29

    @property
    def xsection(self) -> XSection:
        """
        Ensure we only run the water flow simulation once, and return the
        resulting XSection instance.
        """
        try:
            return self._xsection  # pylint: disable=access-member-before-definition
        except AttributeError:
            pass

        xs: XSection = XSection(self.input)
        dq: deque[XY] = deque([xs.water_source])

        row: int
        col: int

        while dq:
            # Get a coordinate off of the queue
            row, col = dq.popleft()

            if xs[row][col] == AT_REST:
                # Water at this coordinate can no longer flow
                continue

            # Move down from the present coordinate until stopped by either the
            # bottom of the grid, or a piece of solid rock.
            row += 1
            while row <= xs.y.max:
                tile: Tile = xs[row][col]

                if tile == EMPTY:
                    # Simulate the stream falling one row by changing this
                    # tile's contents to that of a flowing stream of water.
                    xs[row][col] = FLOWING
                    row += 1

                elif tile in (AT_REST, ROCK):
                    # We've reached either solid rock or water that is at rest.
                    # back up one row, we can't put water into the same space as a
                    # rock or other water.
                    row -= 1

                    # Direction of column spread
                    dx: Literal[-1, 1]
                    # Column numbers spreading both to the left and right
                    adj_col: int
                    # Whether or not the spread of the water overflowed
                    overflow: bool = False
                    # Will store the leftmost and rightmost column that water can
                    # spread horizontally
                    flow_range: list[int] = []

                    # Search in either direction for places where water can
                    # expand. If an overflow is found, add it to the queue to
                    # be processed.
                    for dx in (-1, 1):
                        adj_col = col
                        while True:
                            adj_tile: Tile = xs[row][adj_col]
                            if adj_tile == ROCK:
                                # Horizontal flow has reached a wall, reverse
                                # the column pointer by 1 and exit
                                adj_col -= dx
                                break

                            below_adj_tile: Tile = xs[row + 1][adj_col]
                            if below_adj_tile == EMPTY:
                                # The tile beneath the one we're currently
                                # looking at is empty, this means we've found
                                # an overflow.
                                overflow = True
                                # Add the current position to the queue
                                dq.append((row, adj_col))
                                break

                            # Handle the case where another stream has already
                            # flowed into the current position. This can happen
                            # when a small reservoir fills and overflows on
                            # both sides into a larger one, or a series of
                            # overflows causes one overlowing stream of water
                            # to fall into a place where water has already
                            # overflowed.
                            if adj_tile == below_adj_tile == FLOWING:
                                overflow = True
                                break

                            # Advance a column and repeat the above checks
                            adj_col += dx

                        flow_range.append(adj_col)

                    # Fill in a line of water
                    fill_char: Literal[AT_REST, FLOWING] = AT_REST if not overflow else FLOWING
                    fill_col: int
                    for fill_col in range(flow_range[0], flow_range[1] + 1):
                        xs[row][fill_col] = fill_char

                else:
                    # Flowing water has hit another flow, no need to continue
                    # as it would be redundant to do so.
                    break

        # With the water flow simulated, return the resulting object
        self._xsection: XSection = xs  # pylint: disable=attribute-defined-outside-init
        return self._xsection

    def part1(self) -> int:
        """
        Return the number of tiles that water can reach
        """
        count: Counter = self.xsection.counter(row_start=self.xsection.y.min)
        return count["|"] + count["~"]

    def part2(self) -> int:
        """
        Return the number of tiles containing water at rest
        """
        return self.xsection.counter(row_start=self.xsection.y.min)["~"]


if __name__ == "__main__":
    aoc = AOC2018Day17()
    aoc.run()
