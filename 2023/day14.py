#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/14
'''
# Local imports
from aoc import AOC, Grid

# Typing shortcuts
Pattern = tuple[str]

class Platform(Grid):
    '''
    Represents the platform from 2023 Day 14
    '''
    rounded = 'O'
    cube = '#'
    empty = '.'

    @property
    def load(self) -> int:
        '''
        Calculate the current load on the north support beam
        '''
        return sum(
            (self.rows - cur_row) * self[cur_row].count(self.rounded)
            for cur_row in range(self.rows)
        )

    @property
    def state(self) -> tuple[tuple[str]]:
        '''
        Return the grid as a tuple of tuples, providing a hashable grid state
        '''
        return tuple(tuple(row) for row in self.data)

    def tilt_north(self) -> None:
        '''
        Tilt the platform so that round rocks roll north until they can't move
        any further.
        '''
        # Enumeration is useless here since we are going to be modifying the
        # grid. So, we'll need to use range() to get an index and use list
        # indexing to access the current value of a given position. Note that
        # the 2D array can be indexed off the object itself.
        for row in range(1, self.rows):
            for col in range(self.cols):
                if (
                    self[row][col] == self.rounded
                    and self[row - 1][col] == self.empty
                ):
                    # Current position is a rounded rock and there is space
                    # for it to roll. Find the furthest empty column, which
                    # will be the new position of the rock.
                    for new_row in range(row - 1, 0, -1):
                        if self[new_row - 1][col] != self.empty:
                            break
                    else:
                        new_row = 0

                    # Update the grid, moving the rounded rock to the new
                    # column and setting the old position to empty.
                    self[new_row][col] = self.rounded
                    self[row][col] = self.empty

    def tilt_west(self) -> None:
        '''
        Same concept as north(), but move the rocks to the left instead
        '''
        for row in range(self.rows):
            for col in range(1, self.cols):
                if (
                    self[row][col] == self.rounded
                    and self[row][col - 1] == self.empty
                ):
                    for new_col in range(col - 1, 0, -1):
                        if self[row][new_col - 1] != self.empty:
                            break
                    else:
                        new_col = 0

                    self[row][new_col] = self.rounded
                    self[row][col] = self.empty

    def tilt_south(self) -> None:
        '''
        Same concept as north(), but move the rocks down instead
        '''
        for row in range(self.rows - 2, -1, -1):
            for col in range(self.cols):
                if (
                    self[row][col] == self.rounded
                    and self[row + 1][col] == self.empty
                ):
                    for new_row in range(row + 1, self.rows - 1):
                        if self[new_row + 1][col] != self.empty:
                            break
                    else:
                        new_row = self.rows - 1

                    self[new_row][col] = self.rounded
                    self[row][col] = self.empty

    def tilt_east(self) -> None:
        '''
        Same concept as north(), but move the rocks to the right instead
        '''
        for row in range(self.rows):
            for col in range(self.cols - 2, -1, -1):
                if (
                    self[row][col] == self.rounded
                    and self[row][col + 1] == self.empty
                ):
                    for new_col in range(col + 1, self.cols - 1):
                        if self[row][new_col + 1] != self.empty:
                            break
                    else:
                        new_col = self.cols - 1

                    self[row][new_col] = self.rounded
                    self[row][col] = self.empty


class AOC2023Day14(AOC):
    '''
    Day 14 of Advent of Code 2023
    '''
    day = 14

    def part1(self) -> int:
        '''
        Solve for Part 1
        '''
        platform = Platform(self.input)
        platform.tilt_north()
        return platform.load

    def part2(self) -> int:
        '''
        Solve for Part 2
        '''
        platform = Platform(self.input)

        states = {}
        index = 0
        cycles = 1_000_000_000

        while index < cycles:
            platform.tilt_north()
            platform.tilt_west()
            platform.tilt_south()
            platform.tilt_east()
            index += 1
            state = platform.state
            if state not in states:
                # Save state and index for cycle detection
                states[state] = index
            else:
                # Cycle detected
                period = index - states[state]
                # Skip ahead as many periods as possible
                index += ((cycles - index) // period) * period
                # We've reset the index position, so all of our previous cycle
                # calculations are now invalid.
                states.clear()

        return platform.load


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day14(example=True)
    aoc.validate(aoc.part1(), 136)
    aoc.validate(aoc.part2(), 64)
    # Run against actual data
    aoc = AOC2023Day14(example=False)
    aoc.run()
