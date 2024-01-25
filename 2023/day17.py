#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/17
'''
import heapq
import textwrap
from collections import namedtuple

# Local imports
from aoc import AOC, Grid, XY, TupleMixin


class AOC2023Day17(AOC, TupleMixin):
    '''
    Day 17 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
        '''
    )

    validate_part1: int = 102
    validate_part2: int = 94

    def post_init(self) -> None:
        '''
        Load the input data into a Grid object
        '''
        self.crucible: Grid = Grid(
            self.input,
            lambda col: int(col),  # pylint: disable=unnecessary-lambda
        )

    def solve(
        self,
        min_streak: int = 0,
        max_streak: int = 1e9,
    ) -> int:
        '''
        Calculate minimum heat loss using Dijkstra's Algorithm
        '''
        # Heap will sort on tuples containing the following items:
        #
        #   1. loss - the total heat loss calculated. This comes first to give
        #      it priority in the heap.
        #
        #   2. A namedtuple containing unique location, direction, and streak
        #      values so that we can track what situations we've already
        #      analyzed.

        DijkstraKey = namedtuple(
            'DijkstraKey',
            ('row', 'col', 'direction', 'streak')
        )

        heap: list[tuple[int, DijkstraKey]] = [(0, DijkstraKey(0, 0, None, None))]
        best: int = 1e9
        visited: set[DijkstraKey]  = set()

        while heap:
            loss: int
            state: DijkstraKey
            loss, state = heapq.heappop(heap)

            if state in visited:
                # Prevent duplicate processing
                continue

            # Store the values for this permutation
            visited.add(state)

            # From the perspective of the current coordinate, try every
            # direction. The "directions" namedtuple contains row/column deltas
            # that can be used to calculate movement from one coordinate to
            # another. Another tuple, "opposite_directions", has the same
            # deltas, but with the order for north/south and west/east
            # swappped. Thus, if the index of one direction from the
            # "directions" namedtuple is equal to the index of another
            # direction from the "opposite_directions" namedtuple, we know that
            # the two directions are each other's opposite. This will be used
            # below to check for reverse movement, which is not allowed.
            new_direction: int
            delta: XY
            for new_direction, delta in enumerate(self.crucible.directions):
                opposite: int = self.crucible.opposite_directions[new_direction]
                if (
                    state.direction is not None
                    and self.crucible.directions[state.direction] == opposite
                ):
                    # This direction is the reverse of the previous one, this
                    # is not a valid move.
                    continue

                # Apply deltas to current row/col to get new values
                new_row: int
                new_col: int
                new_row, new_col = self.tuple_add((state.row, state.col), delta)

                # If the direction hasn't changed, the streak continues,
                # otherwise the new streak will reset at 1.
                new_streak: int = (
                    state.streak + 1 if new_direction == state.direction
                    else 1
                )

                # Check for invalid streak. First check if longer than the max
                # allowed streak.
                invalid_streak: bool = new_streak > max_streak

                # If streak is <= the max streak, check if there A) is a
                # minimum streak, and B) the direction has changed.
                if (
                    (not invalid_streak and min_streak)
                    and new_direction != state.direction
                    and state.direction is not None
                ):
                    # Minimum streak is specified, and direction has changed
                    # from the prior step. Streak is therefore invalid if it is
                    # lower than the minimum.
                    invalid_streak: bool = state.streak < min_streak

                if (
                    invalid_streak
                    or (not 0 <= new_row <= self.crucible.max_row)
                    or (not 0 <= new_col <= self.crucible.max_col)
                ):
                    # This step either
                    #
                    #   A) Has a streak that is too short or long (as
                    #      determined above).
                    #
                    #   B) Has exited the bounds of the grid
                    #
                    # In either case, this is not a valid move
                    continue

                # Move is valid. Add heat loss value from current coordinate to
                # the running total to get the updated heat loss value.
                new_loss: int = loss + self.crucible[new_row][new_col]

                if (
                    new_row == self.crucible.max_row
                    and new_col == self.crucible.max_col
                    and (
                        not min_streak
                        or (min_streak and new_streak >= min_streak)
                    )
                ):
                    # We've reached the end of the grid. However, if there is a
                    # min streak and we reach the end of the grid with a streak
                    # lower than the minumum, this is not a valid run. This is
                    # only a valid run if there is no minimum streak, or there
                    # is one and it has been met or exceeded.
                    best: int = min(best, new_loss)

                # This was a valid move, add to the heap so that future loop
                # iterations can build upon it.
                heapq.heappush(
                    heap,
                    (
                        new_loss,
                        DijkstraKey(new_row, new_col, new_direction, new_streak)
                    )
                )

        return best

    def part1(self) -> int:
        '''
        Solve for Part 1. Crucible can only move 3 or fewer spaces at a time in
        the same direction.
        '''
        return self.solve(max_streak=3)

    def part2(self) -> int:
        '''
        Solve for Part 2. Crucible must move at least 4, but no more than 10
        spaces at a time in the same direction.
        '''
        return self.solve(min_streak=4, max_streak=10)


if __name__ == '__main__':
    aoc = AOC2023Day17()
    aoc.run()
