#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/10
'''
import textwrap
from collections import deque
from collections.abc import Iterator, Sequence
from pathlib import Path

# Local imports
from aoc import AOC, Grid, XY


class HikingMap(Grid):
    '''
    Simulate the hiking map
    '''
    def __init__(
        self,
        data: Path | str | Sequence[str],
    ) -> None:
        '''
        Load the file from the Path object
        '''
        super().__init__(data, row_cb=lambda col: int(col))  # pylint: disable=unnecessary-lambda

    @property
    def trailheads(self) -> Iterator[XY]:
        '''
        Yields a sequence of coordinates where trailheads start
        '''
        coord: XY
        value: int
        for coord, value in self.tile_iter():
            if value == 0:
                yield coord


class AOC2024Day10(AOC):
    '''
    Day 10 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        89010123
        78121874
        87430965
        96549874
        45678903
        32019012
        01329801
        10456732
        '''
    )

    validate_part1: int = 36
    validate_part2: int = 81

    def part1(self) -> int:
        '''
        BFS solution to calculate reachable peaks from each trailhead
        '''
        hiking_map: HikingMap = HikingMap(self.input)
        score: int = 0

        start: XY
        for start in hiking_map.trailheads:
            visited: set[XY] = set()
            dq: deque[XY] = deque([start])
            while dq:
                coord: XY = dq.popleft()
                if coord in visited:
                    continue
                elevation: int = hiking_map[coord]
                visited.add(coord)

                if hiking_map[coord] == 9:
                    # We've reached the end of a valid trail, increase score by 1
                    score += 1
                else:
                    # Check each neighbor to see if it is a valid next step
                    neighbor: XY
                    neighbor_elevation: int
                    for neighbor, neighbor_elevation in hiking_map.neighbors(coord):
                        if elevation + 1 == neighbor_elevation:
                            # Only continue to follow this trail if the
                            # neighbor has an elevation 1 greater than the
                            # current elevation.
                            dq.append(neighbor)

        return score

    def part2(self) -> int:
        '''
        BFS solution to get the number of distinct trails that can be derived
        from the puzzle data. This differs slightly from Part 1 in that rather
        than tracking the distinct coordinates visited, we instead need to track
        the sequences of coordinates that make up a distinct trail.
        '''
        # Type hints
        Trail = tuple[XY, ...]

        hiking_map: HikingMap = HikingMap(self.input)
        distinct_trails: set[Trail] = set()

        start: XY
        for start in hiking_map.trailheads:
            visited: set[Trail] = set()
            dq: deque[Trail] = deque([(start,)])
            while dq:
                trail: Trail = dq.popleft()
                if trail in visited:
                    continue
                # Coordinate of most recent step in the trail
                coord: int = trail[-1]
                # Elevation of most recent step in the trail
                elevation: int = hiking_map[coord]
                visited.add(trail)

                if hiking_map[coord] == 9:
                    # We've reached the end of a valid trail. Add the sequence
                    # of positions we traversed to get here to the set where we
                    # are tracking the distinct trails.
                    distinct_trails.add(trail)
                else:
                    # Check each neighbor to see if it is a valid next step
                    neighbor: XY
                    neighbor_elevation: int
                    for neighbor, neighbor_elevation in hiking_map.neighbors(coord):
                        if elevation + 1 == neighbor_elevation:
                            # Only continue to follow this trail if the
                            # neighbor has an elevation 1 greater than the
                            # current elevation.
                            dq.append(trail + (neighbor,))

        return len(distinct_trails)


if __name__ == '__main__':
    aoc = AOC2024Day10()
    aoc.run()
