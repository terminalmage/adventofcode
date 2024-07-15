#!/usr/bin/env python
"""
https://adventofcode.com/2018/day/18
"""
import copy
import textwrap
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Literal

# Local imports
from aoc import AOC, Grid, directions, ordinal_directions


class Tiles:
    """
    Defines possible tile values
    """
    OPEN: str = "."
    TREES: str = "|"
    LUMBERYARD: str = "#"


# Type hints
Tile = Literal[Tiles.OPEN, Tiles.TREES, Tiles.LUMBERYARD]


class MagicForest(Grid):
    """
    Includes a function to simulate the changing contents of the forest
    """
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

    def shift(self):
        """
        Change the contents of the forest per the puzzle rules
        """
        new_data: list[list[Tile]] = copy.deepcopy(self.data)
        row: int
        col: int
        line: list[Tile]
        tile: Tile
        for row, line in enumerate(self.data):
            for col, tile in enumerate(line):
                neighbors: Counter = Counter(
                    n[1] for n in self.neighbors((row, col))
                )
                match tile:
                    case Tiles.OPEN:
                        if neighbors[Tiles.TREES] >= 3:
                            new_data[row][col] = Tiles.TREES
                    case Tiles.TREES:
                        if neighbors[Tiles.LUMBERYARD] >= 3:
                            new_data[row][col] = Tiles.LUMBERYARD
                    case Tiles.LUMBERYARD:
                        if not (neighbors[Tiles.LUMBERYARD] and neighbors[Tiles.TREES]):
                            new_data[row][col] = Tiles.OPEN

        self.data: list[list[Tile]] = new_data


class AOC2018Day18(AOC):
    """
    Day 18 of Advent of Code 2018
    """
    example_data: str = textwrap.dedent(
        """
        .#.#...|#.
        .....#|##|
        .|..|...#.
        ..|#.....#
        #.#|||#|#|
        ...#.||...
        .|....|...
        ||...#|.#|
        |.||||..|.
        ...#.|..|.
        """
    )

    validate_part1: int = 1147

    def part1(self) -> int:
        """
        After 10 shifts, return the number of acres of trees multiplied by the
        number of acres occupied by lumberyards.
        """
        forest: MagicForest = MagicForest(self.input)

        for _ in range(10):
            forest.shift()

        count: Counter = forest.counter()
        return count[Tiles.TREES] * count[Tiles.LUMBERYARD]

    def part2(self) -> int:
        """
        Same as part 1, only return the result after one billion shifts.
        """
        forest: MagicForest = MagicForest(self.input)

        # Track the state after each round, so we can detect the number of
        # rounds that elapse between cycles.
        states: dict[str, int] = {}

        index: int = 0
        shifts: int = 1_000_000_000

        while index < shifts:
            forest.shift()
            index += 1
            sha: str = forest.sha256()
            if sha not in states:
                # Save state and index for cycle detection
                states[sha] = index
            else:
                # Cycle detected
                period: int = index - states[sha]
                # Skip ahead as many periods as possible
                index += ((shifts - index) // period) * period
                # We've reset the index position, so all of our previous cycle
                # calculations are now invalid.
                states.clear()

        count: Counter = forest.counter()
        return count[Tiles.TREES] * count[Tiles.LUMBERYARD]


if __name__ == "__main__":
    aoc = AOC2018Day18()
    aoc.run()
