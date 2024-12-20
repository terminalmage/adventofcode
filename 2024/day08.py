#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/8
'''
import itertools
import textwrap
from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path

# Local imports
from aoc import AOC, Grid, XY


class AntennaMap(Grid):
    '''
    Simulate the antenna map from the puzzle
    '''
    def __init__(
        self,
        data: Path | str | Sequence[str],
    ) -> None:
        '''
        Load the file from the Path object, and then gather all the coordinates
        belonging to each of the antenna frequencies.
        '''
        super().__init__(data)
        pos: XY
        value: str
        self.antennas: defaultdict[set] = defaultdict(set)
        for pos, value in self.tile_iter():
            if value != '.':
                self.antennas[value].add(pos)

    def antinodes(self, resonant: bool = False) -> set[XY]:
        '''
        Yields the position and antenna type for each antinode
        '''
        ret: set[XY] = set()

        positions: set[XY]
        for positions in self.antennas.values():
            first: XY
            second: XY
            candidate: XY
            for (first, second) in itertools.combinations(positions, 2):
                # Calculate the delta needed to move from the first antenna to
                # the second antenna
                delta: XY = self.tuple_subtract(first, second)

                if resonant:

                    # Per the puzzle, all antennas which are not the only
                    # antenna of their kind are also themselves antinodes when
                    # considering resonant harmonics. But if we got to this
                    # point, we know that there were at least two antennas at
                    # this frequency. If there weren't,
                    # itertools.combinations() would not be able to produce a
                    # tuple of length 2 and would yield nothing.
                    ret.update((first, second))

                    # Moving from the second antenna to the position of the
                    # antinodes will involve starting at the point of the
                    # second antenna, and continuing to move in increments of
                    # the same delta. Since we used tuple subtraction to
                    # generate the original delta, continue with subtraction
                    # until we leave the bounds of the grid.
                    ptr: XY = second
                    while (candidate := self.tuple_subtract(ptr, delta)) in self:
                        ret.add(candidate)
                        ptr = candidate

                    # Repeat the above in the opposite direction, starting from
                    # the first antenna. To go the opposite direction, we need
                    # to use tuple addition instead of subtraction.
                    ptr: XY = first
                    while (candidate := self.tuple_add(ptr, delta)) in self:
                        ret.add(candidate)
                        ptr = candidate

                else:

                    # Like above, we need to continue using tuple subtraction
                    # to find the antinode, and reverse using tuple addition to
                    # get the other. The key difference here is that we don't
                    # repeat this until we leave the grid.
                    for candidate in (
                        self.tuple_subtract(second, delta),
                        self.tuple_add(first, delta),
                    ):
                        if candidate in self:
                            ret.add(candidate)
        return ret


class AOC2024Day8(AOC):
    '''
    Day 8 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        ............
        ........0...
        .....0......
        .......0....
        ....0.......
        ......A.....
        ............
        ............
        ........A...
        .........A..
        ............
        ............
        '''
    )

    validate_part1: int = 14
    validate_part2: int = 34

    # Set by post_init
    antenna_map = None

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.antenna_map: AntennaMap = AntennaMap(self.input)

    def part1(self) -> int:
        '''
        Return the number of antinodes
        '''
        return len(self.antenna_map.antinodes())

    def part2(self) -> int:
        '''
        Return the number of antinodes, taking into consideration the behavior
        of resonant harmonics
        '''
        return len(self.antenna_map.antinodes(resonant=True))


if __name__ == '__main__':
    aoc = AOC2024Day8()
    aoc.run()
