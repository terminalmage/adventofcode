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
        Load the file from the Path object
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
                delta: XY = self.tuple_subtract(first, second)

                if resonant:

                    ret.update((first, second))

                    ptr: XY = first
                    while (candidate := self.tuple_add(ptr, delta)) in self:
                        ret.add(candidate)
                        ptr = candidate

                    ptr: XY = second
                    while (candidate := self.tuple_subtract(ptr, delta)) in self:
                        ret.add(candidate)
                        ptr = candidate

                else:

                    for candidate in (
                        self.tuple_add(first, delta),
                        self.tuple_subtract(second, delta),
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
        Return the number of valid equations based on the criteria from Part 1
        '''
        return len(self.antenna_map.antinodes())

    def part2(self) -> int:
        '''
        Return the number of valid equations based on the criteria from Part 2
        '''
        return len(self.antenna_map.antinodes(resonant=True))


if __name__ == '__main__':
    aoc = AOC2024Day8()
    aoc.run()
