#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/17
'''
import heapq

# Local imports
from aoc import AOC, Grid, directions, opposite_directions


class AOC2023Day17(AOC):
    '''
    Day 17 of Advent of Code 2023
    '''
    day = 17

    def __init__(self, example: bool = False) -> None:
        '''
        Load the steps
        '''
        super().__init__(example=example)
        self.crucible = Grid(
            self.input,
            lambda col: int(col),  # pylint: disable=unnecessary-lambda
        )

    def solve(
        self,
        min_streak: int = 0,
        max_streak: int = 1e9,
    ) -> int:
        '''
        Calculate minimum heat loss
        '''
        # Heap will sort on (loss, row, col, direction, streak)
        # - "loss" is the total heat loss calculated. This is at the front of
        #   the queue entry to give it priority when getting values from queue.
        # - "row" and "col" are the location.
        # - "direction" is an integer index from the "directions" namedtuple.
        # - "streak" is the number of times in a row that the Crucible has
        #   traveled in the current direction.
        #
        # Initialize heap with zero/null values
        heap = [(0, 0, 0, None, None)]

        best = 1e9
        max_row = self.crucible.rows - 1
        max_col = self.crucible.cols - 1

        visited = set()
        while heap:
            loss, row, col, direction, streak = heapq.heappop(heap)

            key = (row, col, direction, streak)
            if key in visited:
                # Prevent duplicate processing
                continue

            # Store the values for this permutation
            visited.add(key)

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
            for new_direction, (row_delta, col_delta) in enumerate(directions):
                # pylint: disable=invalid-sequence-index
                if (
                    direction is not None
                    and directions[direction] == opposite_directions[new_direction]
                ):
                    # This direction is the reverse of the previous one, this
                    # is not a valid move.
                    continue
                # pylint: enable=invalid-sequence-index

                # Apply deltas to current row/col to get new values
                new_row, new_col = row + row_delta, col + col_delta

                # If the direction hasn't changed, the streak continues,
                # otherwise the new streak will reset at 1.
                new_streak = streak + 1 if new_direction == direction else 1

                # Check for invalid streak. First check if longer than the max
                # allowed streak.
                invalid_streak = new_streak > max_streak

                # If streak is <= the max streak, check minimum.
                if (
                    (not invalid_streak and min_streak)
                    and new_direction != direction
                    and direction is not None
                ):
                    # Minimum streak is specified, and direction has changed
                    # from the prior step. Streak is therefore invalid if it is
                    # lower than the minimum.
                    invalid_streak = streak < min_streak

                if (
                    invalid_streak
                    or (not 0 <= new_row <= max_row)
                    or (not 0 <= new_col <= max_col)
                ):
                    # This step either
                    #  A) exceeds the max streak (or is less than min streak)
                    #  B) has exited the bounds of the grid
                    continue

                # Move is valid. Add heat loss value from current coordinate to
                # the running total to get the updated heat loss value.
                new_loss = loss + self.crucible[new_row][new_col]

                if (
                    new_row == max_row and new_col == max_col
                    and (
                        not min_streak
                        or (min_streak and new_streak >= min_streak)
                    )
                ):
                    # We've reached the end of the grid. However, if there is a
                    # min streak and we reach the end of the grid with a streak
                    # lower than the minumum, this is not a valid run. Only
                    # consider this a valid run if there is no minimum streak,
                    # or there is one and it has been met or exceeded.
                    best = min(best, new_loss)

                # This was a valid move, add to the heap so that future loop
                # iterations can build upon it.
                heapq.heappush(
                    heap,
                    (new_loss, new_row, new_col, new_direction, new_streak)
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
    # Run against test data
    aoc = AOC2023Day17(example=True)
    aoc.validate(aoc.part1(), 102)
    aoc.validate(aoc.part2(), 94)
    # Run against actual data
    aoc = AOC2023Day17(example=False)
    aoc.run()
