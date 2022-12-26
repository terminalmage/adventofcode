#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/24

--- Day 24: Blizzard Basin ---

With everything replanted for next year (and with elephants and monkeys to tend
the grove), you and the Elves leave for the extraction point.

Partway up the mountain that shields the grove is a flat, open area that serves
as the extraction point. It's a bit of a climb, but nothing the expedition
can't handle.

At least, that would normally be true; now that the mountain is covered in
snow, things have become more difficult than the Elves are used to.

As the expedition reaches a valley that must be traversed to reach the
extraction site, you find that strong, turbulent winds are pushing small
blizzards of snow and sharp ice around the valley. It's a good thing everyone
packed warm clothes! To make it across safely, you'll need to find a way to
avoid them.

Fortunately, it's easy to see all of this from the entrance to the valley, so
you make a map of the valley and the blizzards (your puzzle input). For
example:

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#

The walls of the valley are drawn as #; everything else is ground. Clear ground
- where there is currently no blizzard - is drawn as .. Otherwise, blizzards
are drawn with an arrow indicating their direction of motion: up (^), down (v),
left (<), or right (>).

The above map includes two blizzards, one moving right (>) and one moving down
(v). In one minute, each blizzard moves one position in the direction it is
pointing:

#.#####
#.....#
#.>...#
#.....#
#.....#
#...v.#
#####.#

Due to conservation of blizzard energy, as a blizzard reaches the wall of the
valley, a new blizzard forms on the opposite side of the valley moving in the
same direction. After another minute, the bottom downward-moving blizzard has
been replaced with a new downward-moving blizzard at the top of the valley
instead:

#.#####
#...v.#
#..>..#
#.....#
#.....#
#.....#
#####.#

Because blizzards are made of tiny snowflakes, they pass right through each
other. After another minute, both blizzards temporarily occupy the same
position, marked 2:

#.#####
#.....#
#...2.#
#.....#
#.....#
#.....#
#####.#

After another minute, the situation resolves itself, giving each blizzard back
its personal space:

#.#####
#.....#
#....>#
#...v.#
#.....#
#.....#
#####.#

Finally, after yet another minute, the rightward-facing blizzard on the right
is replaced with a new one on the left facing the same direction:

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#

This process repeats at least as long as you are observing it, but probably
forever.

Here is a more complex example:

#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#

Your expedition begins in the only non-wall position in the top row and needs
to reach the only non-wall position in the bottom row. On each minute, you can
move up, down, left, or right, or you can wait in place. You and the blizzards
act simultaneously, and you cannot share a position with a blizzard.

In the above example, the fastest way to reach your goal requires 18 steps.
Drawing the position of the expedition as E, one way to achieve this is:

Initial state:
#E######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#

Minute 1, move down:
#.######
#E>3.<.#
#<..<<.#
#>2.22.#
#>v..^<#
######.#

Minute 2, move down:
#.######
#.2>2..#
#E^22^<#
#.>2.^>#
#.>..<.#
######.#

Minute 3, wait:
#.######
#<^<22.#
#E2<.2.#
#><2>..#
#..><..#
######.#

Minute 4, move up:
#.######
#E<..22#
#<<.<..#
#<2.>>.#
#.^22^.#
######.#

Minute 5, move right:
#.######
#2Ev.<>#
#<.<..<#
#.^>^22#
#.2..2.#
######.#

Minute 6, move right:
#.######
#>2E<.<#
#.2v^2<#
#>..>2>#
#<....>#
######.#

Minute 7, move down:
#.######
#.22^2.#
#<vE<2.#
#>>v<>.#
#>....<#
######.#

Minute 8, move left:
#.######
#.<>2^.#
#.E<<.<#
#.22..>#
#.2v^2.#
######.#

Minute 9, move up:
#.######
#<E2>>.#
#.<<.<.#
#>2>2^.#
#.v><^.#
######.#

Minute 10, move right:
#.######
#.2E.>2#
#<2v2^.#
#<>.>2.#
#..<>..#
######.#

Minute 11, wait:
#.######
#2^E^2>#
#<v<.^<#
#..2.>2#
#.<..>.#
######.#

Minute 12, move down:
#.######
#>>.<^<#
#.<E.<<#
#>v.><>#
#<^v^^>#
######.#

Minute 13, move down:
#.######
#.>3.<.#
#<..<<.#
#>2E22.#
#>v..^<#
######.#

Minute 14, move right:
#.######
#.2>2..#
#.^22^<#
#.>2E^>#
#.>..<.#
######.#

Minute 15, move right:
#.######
#<^<22.#
#.2<.2.#
#><2>E.#
#..><..#
######.#

Minute 16, move right:
#.######
#.<..22#
#<<.<..#
#<2.>>E#
#.^22^.#
######.#

Minute 17, move down:
#.######
#2.v.<>#
#<.<..<#
#.^>^22#
#.2..2E#
######.#

Minute 18, move down:
#.######
#>2.<.<#
#.2v^2<#
#>..>2>#
#<....>#
######E#

What is the fewest number of minutes required to avoid the blizzards and reach
the goal?

--- Part Two ---

As the expedition reaches the far side of the valley, one of the Elves looks
especially dismayed:

He forgot his snacks at the entrance to the valley!

Since you're so good at dodging blizzards, the Elves humbly request that you go
back for his snacks. From the same initial conditions, how quickly can you make
it from the start to the goal, then back to the start, then back to the goal?

In the above example, the first trip to the goal takes 18 minutes, the trip
back to the start takes 23 minutes, and the trip back to the goal again takes
13 minutes, for a total time of 54 minutes.

What is the fewest number of minutes required to reach the goal, go back to the
start, then reach the goal again?

'''
import collections
import functools

# Local imports
from aoc2022 import AOC2022

# Right, down, wait, left, up
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STAY_PUT = (0, 0)
MOVES = (UP, DOWN, LEFT, RIGHT, STAY_PUT)

# Typing shortcuts
Coordinate = tuple[int, int]


class AOC2022Day24(AOC2022):
    '''
    Day 24 of Advent of Code 2022
    '''
    day = 24

    def __init__(self, example: bool = False) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        super().__init__(example=example)
        with self.input.open() as fh:
            lines = fh.read().splitlines()[1:-1]

        blizzard_map = {'^': 'up', 'v': 'down', '<': 'left', '>': 'right'}
        blizzards = {direction: set() for direction in blizzard_map.values()}

        for row, line in enumerate(lines):
            for col, item in enumerate(line[1:-1]):
                if item in blizzard_map:
                    blizzards[blizzard_map[item]].add((col, row))

        for direction, coords in blizzards.items():
            setattr(self, f'{direction}_blizzards', frozenset(coords))

        self.height = len(lines)
        self.width = len(lines[0]) - 2

        self.entrance = (0, 0)
        self.exit = (self.width - 1, self.height - 1)

    def can_move(
        self,
        position: Coordinate,
        timestamp: int,
    ) -> bool:
        '''
        Since blizzards wrap around in each direction, their positions can be
        represented as their original position plus the timestamp, modulo the
        height/width of the grid
        '''
        col, row = position
        # pylint: disable=no-member
        return not any((
            (col, (row + timestamp) % self.height) in self.up_blizzards,
            (col, (row - timestamp) % self.height) in self.down_blizzards,
            ((col + timestamp) % self.width, row) in self.left_blizzards,
            ((col - timestamp) % self.width, row) in self.right_blizzards,
        ))
        # pylint: enable=no-member

    def bfs(
        self,
        start: Coordinate | None = None,
        end: Coordinate | None = None,
        init_timestamp: int = 0,
    ) -> int:
        '''
        Use breadth-first search to find time spent in shortest path
        '''
        start = start or self.entrance
        end = end or self.exit

        visited = set()

        dq = collections.deque()

        while True:
            while not dq:
                # Ensure we count the first minute(s), in which we can either
                # A) enter the valley, or B) wait for blizzard(s) to pass
                init_timestamp += 1
                # Check to see if the coast is clear
                if self.can_move(start, init_timestamp):
                    dq.append((start, init_timestamp))

            coord, timestamp = dq.popleft()

            if (coord, timestamp) in visited:
                continue

            visited.add((coord, timestamp))
            if coord == end:
                return timestamp + 1  # Add a second to factor in the final step

            for delta in MOVES:
                # Only consider moves that are within the bounds, and which are
                # not blocked by a blizzard
                new_pos = tuple(sum(x) for x in zip(coord, delta))
                if (
                    0 <= new_pos[0] < self.width and
                    0 <= new_pos[1] < self.height and
                    self.can_move(new_pos, timestamp + 1)
                ):
                    dq.append((new_pos, timestamp + 1))

    @functools.lru_cache
    def part1(self) -> int:
        '''
        Calculate the quickest you can get from the start to the end
        '''
        return self.bfs()

    def part2(self) -> int:
        '''
        Calculate the quickest you can get from start to end and back again
        '''
        return self.bfs(
            init_timestamp=self.bfs(
                start=self.exit,
                end=self.entrance,
                init_timestamp=self.part1(),
            ),
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day24(example=True)
    aoc.validate(aoc.part1(), 18)
    aoc.validate(aoc.part2(), 54)
    # Run against actual data
    aoc = AOC2022Day24(example=False)
    aoc.run()
