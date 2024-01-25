#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/9
'''
from __future__ import annotations
import textwrap

# Local imports
from aoc import AOC, XY


class Knot:
    '''
    Stores information about current position and all the coordinates the knot
    has visited
    '''
    def __init__(self, start_col: int = 0, start_row: int = 0) -> None:
        '''
        Set the initial position of the knot
        '''
        self.col: int = start_col
        self.row: int = start_row
        self.visited: set[XY] = {(self.col, self.row)}

    def __eq__(self, other: Knot) -> bool:
        '''
        Implement == operator
        '''
        return self.col == other.col and self.row == other.row

    @property
    def pos(self) -> XY:
        '''
        Return the current grid position
        '''
        return self.col, self.row

    def move(self, col_delta: int, row_delta: int) -> None:
        '''
        Move the knot. The move will be a no-op if both deltas are 0
        '''
        if col_delta or row_delta:
            if abs(col_delta) > 1 or abs(row_delta) > 1:
                raise ValueError(f'Invalid move ({col_delta}, {row_delta})')

            self.col += col_delta
            self.row += row_delta
            self.visited.add(self.pos)

    def move_next_to(self, other: Knot) -> None:
        '''
        Check if adjacent to the Knot passed in, and if not, move
        '''
        if self == other:
            # Head and tail are in the same position
            return

        def _lateral_delta(first: int, second: int) -> int:
            '''
            Get the delta for a horizontal/vertical move
            '''
            delta: int = first - second
            abs_delta: int = abs(delta)
            if abs_delta <= 1:
                return 0

            ret: int = abs_delta - 1
            return ret if delta > 0 else -ret

        if self.col == other.col:
            # Vertical move
            self.move(0, _lateral_delta(other.row, self.row))
        elif self.row == other.row:
            # Horizontal move
            self.move(_lateral_delta(other.col, self.col), 0)
        else:
            col_delta: int = other.col - self.col
            row_delta: int = other.row - self.row
            if abs(col_delta) == abs(row_delta) == 1:
                # Diagonally adjacent, no move necessary
                return
            self.move(
                -1 if col_delta < 0 else 1,
                -1 if row_delta < 0 else 1,
            )

class AOC2022Day9(AOC):
    '''
    Day 9 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        R 4
        U 4
        L 3
        D 1
        R 4
        D 1
        L 5
        R 2
        '''
    )

    validate_part1: int = 13
    validate_part2: int = 1

    def post_init(self) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        self.moves: list[tuple[XY, int]] = []

        for line in self.input.splitlines():
            direction, distance = line.split()
            match direction:
                case 'R':
                    move = (1, 0)
                case 'L':
                    move = (-1, 0)
                case 'U':
                    move = (0, 1)
                case 'D':
                    move = (0, -1)
                case _:
                    raise ValueError(f'Invalid direction: {direction!r}')

            self.moves.append((move, int(distance)))

    def apply_moves(self, num_knots: int) -> int:
        '''
        Run through the moves given the specified number of knots. Return the
        number of distinct coordinates that the tail visits.
        '''
        if num_knots < 2:
            raise ValueError('num_knots must be >= 2')

        knots: list[Knot] = [Knot() for _ in range(num_knots)]

        move: XY
        distance: int
        for move, distance in self.moves:
            for _ in range(distance):
                knots[0].move(*move)
                index: int
                for index in range(1, num_knots):
                    knots[index].move_next_to(knots[index - 1])

        return len(knots[-1].visited)

    def part1(self) -> int:
        '''
        Run the simulation with 2 knots
        '''
        return self.apply_moves(num_knots=2)

    def part2(self) -> int:
        '''
        Run the simulation with 10 knots
        '''
        return self.apply_moves(num_knots=10)


if __name__ == '__main__':
    aoc = AOC2022Day9()
    aoc.run()
