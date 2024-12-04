#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/4
'''
import textwrap
from collections import Counter
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

# Local imports
from aoc import AOC, XY, Grid, directions, ordinal_directions

# Type hints
Location = XY
Direction = XY
Match = tuple[Location, Direction]


class WordSearch(Grid):
    '''
    Grid subclass with additional functions to locate instances of XMAS
    '''
    def __init__(
        self,
        data: Path | str | Sequence[str],
    ) -> None:
        """
        Modify the default directions to include ordinal directions
        """
        super().__init__(
            data=data,
            neighbor_order=directions + ordinal_directions,
        )

    def findall(self, value: str) -> Iterator[XY]:
        '''
        Return all coordinates matching the specified value
        '''
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == value:
                    yield (row, col)

    def neighbors(self, coord: XY) -> Iterator[tuple[XY, XY, Any]]:
        '''
        Generator which yields the following for each neighboring coordinate:

        1. direction, represented as an XY delta
        2. neighboring coordinate
        3. value stored at that coordinate
        '''
        delta: XY
        for delta in self.directions:
            neighbor: XY = self.tuple_add(coord, delta)
            if neighbor in self:
                yield delta, neighbor, self[neighbor]

    def matches(self, word: str) -> list[Match]:
        '''
        Given the specified word, return a list of coordinates and
        directionality for each match of that word.
        '''
        ret: list[Match] = []
        start: XY
        for start in self.findall(word[0]):
            direction: XY
            neighbor: XY
            value: str
            # Look in all directions for the 2nd letter of the word
            for direction, neighbor, value in self.neighbors(start):
                if value == word[1]:
                    # We've found it, now continue in that direction until we
                    # we discover if we've found a match for the word.
                    cursor: XY = neighbor
                    letter: str
                    for letter in word[2:]:
                        cursor = self.tuple_add(cursor, direction)
                        try:
                            if self[cursor] != letter:
                                # Not a match for the next letter in the word,
                                # break out of the loop.
                                break
                        except IndexError:
                            # We've reached the edge of the grid without
                            # finishing the word, treat this as a non-match.
                            break
                    else:
                        ret.append((start, direction))

        return ret


class AOC2024Day4(AOC):
    '''
    Day 4 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        '''
    )

    validate_part1: int = 18
    validate_part2: int = 9

    # Set by post_init
    wordsearch = None

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.wordsearch = WordSearch(self.input)

    def part1(self) -> int:
        '''
        Return number of XMASes
        '''
        return len(self.wordsearch.matches('XMAS'))

    def part2(self) -> int:
        '''
        Return number of X-MASes

        Observations:

          1. An X-MAS can only be made up of two diagonal "MAS" instances which
             intersect (i.e. no horizontal/vertical intersections).

          2. Therefore, if we get the coordinates of the "A" in each *diagonal*
             "MAS" match, the number of "A" coordinates which appear in more
             than one match is equal to the number of X-MAS instances.

          3. To get the "A" coordinates, we just need to add the directional
             delta to the location of each "MAS" match.

          4. All diagonal directions are made up of combinations of 1 and -1.
             Thus, a quick-and-dirty test to identify a diagonal "MAS" match
             would be to pass that delta to all(), as any zeros in the
             directional delta would cause all() to return False.

        '''
        a_coords: Counter = Counter(
            self.wordsearch.tuple_add(location, direction)
            for location, direction in self.wordsearch.matches('MAS')
            if all(direction)
        )
        return sum(1 for x in a_coords.values() if x != 1)


if __name__ == '__main__':
    aoc = AOC2024Day4()
    aoc.run()
