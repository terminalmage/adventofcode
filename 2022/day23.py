#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/23
'''
import collections
import itertools
import sys

# Local imports
from aoc import AOC

# Typing shortcuts
Coordinate = tuple[int, int]

# NOTE: Y-axis inverted because we read in the grid from top to bottom
N = (0, -1)
S = (0, 1)
W = (-1, 0)
E = (1, 0)
NW = (-1, -1)
NE = (1, -1)
SW = (-1, 1)
SE = (1, 1)


class AOC2022Day23(AOC):
    '''
    Day 23 of Advent of Code 2022
    '''
    day = 23

    def __init__(self, example: bool = False) -> None:
        '''
        Load the initial elf arrangement into a set
        '''
        super().__init__(example=example)
        self.elves = set()
        all_directions = tuple(
            coord for coord in itertools.product((-1, 0, 1), repeat=2)
            if coord != (0, 0)
        )
        self.isolated = lambda elf: all(
            tuple(sum(x) for x in zip(elf, direction)) not in self.elves
            for direction in all_directions
        )
        self.reset()

    def reset(self):
        '''
        Load the initial state of the elves, as well as that of the moves
        '''
        self.elves.clear()
        with self.input.open() as fh:
            for row, line in enumerate(fh):
                for col, item in enumerate(line.rstrip()):
                    if item == '#':
                        self.elves.add((col, row))

        self.moves = collections.deque(
            (
                ((NW, N, NE), N, 'North'),
                ((SW, S, SE), S, 'South'),
                ((NW, W, SW), W, 'West'),
                ((NE, E, SE), E, 'East'),
            )
        )

    def propose_move(self, elf: Coordinate) -> Coordinate | None:
        '''
        For an elf at the specified coordinate, return the proposed move
        '''
        if not self.isolated(elf):
            for view_cone, move_delta, _ in self.moves:
                for direction in view_cone:
                    if tuple(sum(x) for x in zip(elf, direction)) in self.elves:
                        # Stop checking this view cone, it's occupied
                        break
                else:
                    return tuple(sum(x) for x in zip(elf, move_delta))
        return None

    def call_for_proposals(self):
        '''
        Generate proposed moves for each elf according to the movement rules:

        - If there is no Elf in the N, NE, or NW adjacent positions, the Elf
          proposes moving north one step.

        - If there is no Elf in the S, SE, or SW adjacent positions, the Elf
          proposes moving south one step.

        - If there is no Elf in the W, NW, or SW adjacent positions, the Elf
          proposes moving west one step.

        - If there is no Elf in the E, NE, or SE adjacent positions, the Elf
          proposes moving east one step.

        Moves will not be considered if multiple elves propose moving to the
        same coordinate.
        '''
        moves = collections.defaultdict(list)
        for coord in self.elves:
            move = self.propose_move(coord)
            if move is not None:
                moves[move].append(coord)

        for new_pos in list(moves):
            if len(moves[new_pos]) > 1:
                del moves[new_pos]

        return {x[0]: y for y, x in moves.items()}

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        '''
        Return the min/max x and t coordinates
        '''
        return (
            min(x for (x, y) in self.elves),
            max(x for (x, y) in self.elves),
            min(y for (x, y) in self.elves),
            max(y for (x, y) in self.elves),
        )

    def print(self) -> None:
        '''
        Print the current state of the elves
        '''
        min_x, max_x, min_y, max_y = self.bounds
        for row in range(min_y, max_y + 1):
            for col in range(min_x, max_x + 1):
                sys.stdout.write('#' if (col, row) in self.elves else '.')
            sys.stdout.write('\n')
        sys.stdout.write('\n')

    def part1(self) -> int:
        '''
        Move the elves 10 times and report on the number of empty tiles in the
        square containing all elves
        '''
        self.reset()
        for _ in range(10):
            for old_pos, new_pos in self.call_for_proposals().items():
                self.elves.remove(old_pos)
                self.elves.add(new_pos)
            # Rotate the deque for the next round, so the elves are looking in
            # the correct directions
            self.moves.rotate(-1)

        min_x, max_x, min_y, max_y = self.bounds
        return (max_x - min_x + 1) * (max_y - min_y + 1) - len(self.elves)

    def part2(self) -> int:  # pylint: disable=inconsistent-return-statements
        '''
        Figure out the correct value to use for the "humn" variable, to make
        the two components of the root monkey's equation equal
        '''
        self.reset()
        for index in itertools.count(1):
            proposals = self.call_for_proposals()
            if not proposals:
                return index
            for old_pos, new_pos in proposals.items():
                self.elves.remove(old_pos)
                self.elves.add(new_pos)
            # Rotate the deque for the next round, so the elves are looking in
            # the correct directions
            self.moves.rotate(-1)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day23(example=True)
    aoc.validate(aoc.part1(), 110)
    aoc.validate(aoc.part2(), 20)
    # Run against actual data
    aoc = AOC2022Day23(example=False)
    aoc.run()
