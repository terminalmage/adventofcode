#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/18
'''
import itertools
import textwrap

# Local imports
from aoc import AOC, XY

# Typing shortcuts
Coordinate = tuple[int, int]


class AOC2015Day18(AOC):
    '''
    Day 18 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        .#.#.#
        ...##.
        #....#
        ..#...
        #.#..#
        ####..
        '''
    )

    validate_part1: int = 4
    validate_part2: int = 17

    def animate(self, rounds: int, stuck_corners: bool = False) -> int:
        '''
        Animate the grid for the specified number of rounds, and returns the
        number of lights which are lit after the specified number of rounds.
        '''
        # Load the initial state of the grid
        grid: set[XY] = set()
        row: int
        col: int
        line: str
        char: str
        for row, line in enumerate(self.input.splitlines()):
            for col, char in enumerate(line.rstrip()):
                if char == '#':
                    grid.add((col, row))

        # The grid is a square, get the size of the first row
        size: int = len(self.input.splitlines()[0])

        corners: frozenset[XY] = frozenset(itertools.product((0, size-1), repeat=2))
        if stuck_corners:
            # Make sure the corners are turned on
            grid |= corners

        def neighbors(coord: Coordinate) -> tuple[list[Coordinate]]:
            '''
            Return the neighboring coordinates which are within the grid. Two
            sequences are returned, the ones which are lit, and the ones which
            are not lit.
            '''
            lit: list[XY] = []
            unlit: list[XY] = []

            delta: XY
            for delta in itertools.product((-1, 0, 1), repeat=2):
                if delta == (0, 0):
                    continue  # Not an actual neighbor, skip
                neighbor = tuple(map(sum, zip(coord, delta)))
                if any(not 0 <= index < size for index in neighbor):
                    continue  # Out of bounds
                if neighbor in grid:
                    lit.append(neighbor)
                else:
                    unlit.append(neighbor)

            return lit, unlit

        for _ in range(rounds):
            turn_off: set[XY] = set()
            to_check: set[XY] = set()

            for light in grid:
                lit, unlit = neighbors(light)
                to_check.update(unlit)
                if stuck_corners and light in corners:
                    continue
                if len(lit) not in (2, 3):
                    turn_off.add(light)

            turn_on = {
                coord for coord in to_check
                if len(neighbors(coord)[0]) == 3
            }

            grid -= turn_off
            grid |= turn_on

        return len(grid)

    def part1(self) -> int:
        '''
        Calculate the number of lights lit after the specified number of rounds
        '''
        return self.animate(rounds=4 if self.example else 100)

    def part2(self) -> int:
        '''
        Calculate the number of lights lit after the specified number of
        rounds, with the four corners stuck in the "on" position.
        '''
        return self.animate(
            rounds=5 if self.example else 100,
            stuck_corners=True,
        )


if __name__ == '__main__':
    aoc = AOC2015Day18()
    aoc.run()
