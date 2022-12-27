#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/23

--- Day 23: Unstable Diffusion ---

You enter a large crater of gray dirt where the grove is supposed to be. All
around you, plants you imagine were expected to be full of fruit are instead
withered and broken. A large group of Elves has formed in the middle of the
grove.

"...but this volcano has been dormant for months. Without ash, the fruit can't
grow!"

You look up to see a massive, snow-capped mountain towering above you.

"It's not like there are other active volcanoes here; we've looked everywhere."

"But our scanners show active magma flows; clearly it's going somewhere."

They finally notice you at the edge of the grove, your pack almost overflowing
from the random star fruit you've been collecting. Behind you, elephants and
monkeys explore the grove, looking concerned. Then, the Elves recognize the ash
cloud slowly spreading above your recent detour.

"Why do you--" "How is--" "Did you just--"

Before any of them can form a complete question, another Elf speaks up: "Okay,
new plan. We have almost enough fruit already, and ash from the plume should
spread here eventually. If we quickly plant new seedlings now, we can still
make it to the extraction point. Spread out!"

The Elves each reach into their pack and pull out a tiny plant. The plants rely
on important nutrients from the ash, so they can't be planted too close
together.

There isn't enough time to let the Elves figure out where to plant the
seedlings themselves; you quickly scan the grove (your puzzle input) and note
their positions.

For example:

....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..

The scan shows Elves # and empty ground .; outside your scan, more empty ground
extends a long way in every direction. The scan is oriented so that north is
up; orthogonal directions are written N (north), S (south), W (west), and E
(east), while diagonal directions are written NE, NW, SE, SW.

The Elves follow a time-consuming process to figure out where they should each
go; you can speed up this process considerably. The process consists of some
number of rounds during which Elves alternate between considering where to move
and actually moving.

During the first half of each round, each Elf considers the eight positions
adjacent to themself. If no other Elves are in one of those eight positions,
the Elf does not do anything during this round. Otherwise, the Elf looks in
each of four directions in the following order and proposes moving one step in
the first valid direction:

- If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes
  moving north one step.

- If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes
  moving south one step.

- If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes
  moving west one step.

- If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes
  moving east one step.

After each Elf has had a chance to propose a move, the second half of the round
can begin. Simultaneously, each Elf moves to their proposed destination tile if
they were the only Elf to propose moving to that position. If two or more Elves
propose moving to the same position, none of those Elves move.

Finally, at the end of the round, the first direction the Elves considered is
moved to the end of the list of directions. For example, during the second
round, the Elves would try proposing a move to the south first, then west, then
east, then north. On the third round, the Elves would first consider west, then
east, then north, then south.

As a smaller example, consider just these five Elves:

.....
..##.
..#..
.....
..##.
.....

The northernmost two Elves and southernmost two Elves all propose moving north,
while the middle Elf cannot move north and proposes moving south. The middle
Elf proposes the same destination as the southwest Elf, so neither of them
move, but the other three do:

..##.
.....
..#..
...#.
..#..
.....

Next, the northernmost two Elves and the southernmost Elf all propose moving
south. Of the remaining middle two Elves, the west one cannot move south and
proposes moving west, while the east one cannot move south or west and proposes
moving east. All five Elves succeed in moving to their proposed positions:

.....
..##.
.#...
....#
.....
..#..

Finally, the southernmost two Elves choose not to move at all. Of the remaining
three Elves, the west one proposes moving west, the east one proposes moving
east, and the middle one proposes moving north; all three succeed in moving:

..#..
....#
#....
....#
.....
..#..

At this point, no Elves need to move, and so the process ends.

The larger example above proceeds as follows:

== Initial State ==
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............

== End of Round 1 ==
..............
.......#......
.....#...#....
...#..#.#.....
.......#..#...
....#.#.##....
..#..#.#......
..#.#.#.##....
..............
....#..#......
..............
..............

== End of Round 2 ==
..............
.......#......
....#.....#...
...#..#.#.....
.......#...#..
...#..#.#.....
.#...#.#.#....
..............
..#.#.#.##....
....#..#......
..............
..............

== End of Round 3 ==
..............
.......#......
.....#....#...
..#..#...#....
.......#...#..
...#..#.#.....
.#..#.....#...
.......##.....
..##.#....#...
...#..........
.......#......
..............

== End of Round 4 ==
..............
.......#......
......#....#..
..#...##......
...#.....#.#..
.........#....
.#...###..#...
..#......#....
....##....#...
....#.........
.......#......
..............

== End of Round 5 ==
.......#......
..............
..#..#.....#..
.........#....
......##...#..
.#.#.####.....
...........#..
....##..#.....
..#...........
..........#...
....#..#......
..............

After a few more rounds...

== End of Round 10 ==
.......#......
...........#..
..#.#..#......
......#.......
...#.....#..#.
.#......##....
.....##.......
..#........#..
....#.#..#....
..............
....#..#..#...
..............

To make sure they're on the right track, the Elves like to check after round 10
that they're making good progress toward covering enough ground. To do this,
count the number of empty ground tiles contained by the smallest rectangle that
contains every Elf. (The edges of the rectangle should be aligned to the
N/S/E/W directions; the Elves do not have the patience to calculate arbitrary
rectangles.) In the above example, that rectangle is:

......#.....
..........#.
.#.#..#.....
.....#......
..#.....#..#
#......##...
....##......
.#........#.
...#.#..#...
............
...#..#..#..

In this region, the number of empty ground tiles is 110.

Simulate the Elves' process and find the smallest rectangle that contains the
Elves after 10 rounds. How many empty ground tiles does that rectangle contain?

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
