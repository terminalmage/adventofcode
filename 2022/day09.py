#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/9

--- Day 9: Rope Bridge ---

This rope bridge creaks as you walk along it. You aren't sure how old it is, or
whether it can even support your weight.

It seems to support the Elves just fine, though. The bridge spans a gorge which
was carved out by the massive river far below you.

You step carefully; as you do, the ropes stretch and twist. You decide to
distract yourself by modeling rope physics; maybe you can even figure out where
not to step.

Consider a rope with a knot at each end; these knots mark the head and the tail
of the rope. If the head moves far enough away from the tail, the tail is
pulled toward the head.

Due to nebulous reasoning involving Planck lengths, you should be able to model
the positions of the knots on a two-dimensional grid. Then, by following a
hypothetical series of motions (your puzzle input) for the head, you can
determine how the tail will move.

Due to the aforementioned Planck lengths, the rope must be quite short; in
fact, the head (H) and tail (T) must always be touching (diagonally adjacent
and even overlapping both count as touching):

....
.TH.
....

....
.H..
..T.
....

...
.H. (H covers T)
...

If the head is ever two steps directly up, down, left, or right from the tail,
the tail must also move one step in that direction so it remains close enough:

.....    .....    .....
.TH.. -> .T.H. -> ..TH.
.....    .....    .....

...    ...    ...
.T.    .T.    ...
.H. -> ... -> .T.
...    .H.    .H.
...    ...    ...

Otherwise, if the head and tail aren't touching and aren't in the same row or
column, the tail always moves one step diagonally to keep up:

.....    .....    .....
.....    ..H..    ..H..
..H.. -> ..... -> ..T..
.T...    .T...    .....
.....    .....    .....

.....    .....    .....
.....    .....    .....
..H.. -> ...H. -> ..TH.
.T...    .T...    .....
.....    .....    .....

You just need to work out where the tail goes as the head follows a series of
motions. Assume the head and the tail both start at the same position,
overlapping.

For example:

R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2

This series of motions moves the head right four steps, then up four steps,
then left three steps, then down one step, and so on. After each step, you'll
need to update the position of the tail if the step means the head is no longer
adjacent to the tail. Visually, these motions occur as follows (s marks the
starting position as a reference point):

== Initial State ==

......
......
......
......
H.....  (H covers T, s)

== R 4 ==

......
......
......
......
TH....  (T covers s)

......
......
......
......
sTH...

......
......
......
......
s.TH..

......
......
......
......
s..TH.

== U 4 ==

......
......
......
....H.
s..T..

......
......
....H.
....T.
s.....

......
....H.
....T.
......
s.....

....H.
....T.
......
......
s.....

== L 3 ==

...H..
....T.
......
......
s.....

..HT..
......
......
......
s.....

.HT...
......
......
......
s.....

== D 1 ==

..T...
.H....
......
......
s.....

== R 4 ==

..T...
..H...
......
......
s.....

..T...
...H..
......
......
s.....

......
...TH.
......
......
s.....

......
....TH
......
......
s.....

== D 1 ==

......
....T.
.....H
......
s.....

== L 5 ==

......
....T.
....H.
......
s.....

......
....T.
...H..
......
s.....

......
......
..HT..
......
s.....

......
......
.HT...
......
s.....

......
......
HT....
......
s.....

== R 2 ==

......
......
.H....  (H covers T)
......
s.....

......
......
.TH...
......
s.....

After simulating the rope, you can count up all of the positions the tail
visited at least once. In this diagram, s again marks the starting position
(which the tail also visited) and # marks other positions the tail visited:

..##..
...##.
.####.
....#.
s###..

So, there are 13 positions the tail visited at least once.

Simulate your complete hypothetical series of motions. How many positions does
the tail of the rope visit at least once?

'''
from __future__ import annotations

# Local imports
from aoc2022 import AOC2022


class Knot:
    def __init__(self, start_col: int = 0, start_row: int = 0) -> None:
        '''
        Set the initial position of the knot
        '''
        self.col = start_col
        self.row = start_row
        self.visited = {(self.col, self.row)}

    def __eq__(self, other: Knot) -> bool:
        '''
        Implement == operator
        '''
        return self.col == other.col and self.row == other.row

    @property
    def pos(self) -> tuple[int, int]:
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
            delta = first - second
            abs_delta = abs(delta)
            if abs_delta <= 1:
                return 0
            else:
                ret = abs_delta - 1
                return ret if delta > 0 else -ret

        if self.col == other.col:
            # Vertical move
            self.move(0, _lateral_delta(other.row, self.row))
        elif self.row == other.row:
            # Horizontal move
            self.move(_lateral_delta(other.col, self.col), 0)
        else:
            col_delta = other.col - self.col
            row_delta = other.row - self.row
            if abs(col_delta) == abs(row_delta) == 1:
                # Diagonally adjacent, no move necessary
                return
            self.move(
                -1 if col_delta < 0 else 1,
                -1 if row_delta < 0 else 1,
            )

class AOC2022Day9(AOC2022):
    '''
    Base class for Day 9 of Advent of Code 2022
    '''
    day = 9

    def __init__(self, example: bool = False) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        super().__init__(example=example)

        self.moves = []

        with self.input.open() as fh:
            for line in fh:
                direction, distance = line.rstrip('\n').split()
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

    def run(self, num_knots: int) -> int:
        '''
        Run through the moves given the specified number of knots. Return the
        number of distinct coordinates that the tail visits.
        '''
        if num_knots < 2:
            raise ValueError('num_knots must be >= 2')

        knots = [Knot() for _ in range(num_knots)]

        for move, distance in self.moves:
            for _ in range(distance):
                knots[0].move(*move)
                for index in range(1, num_knots):
                    knots[index].move_next_to(knots[index - 1])

        return len(knots[-1].visited)


if __name__ == '__main__':
    aoc = AOC2022Day9()
    print(f'Answer 1 (2 knots): {aoc.run(num_knots=2)}')
    print(f'Answer 2 (10 knots): {aoc.run(num_knots=10)}')
