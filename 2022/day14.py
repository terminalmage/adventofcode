#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/14

--- Day 14: Regolith Reservoir ---

The distress signal leads you to a giant waterfall! Actually, hang on - the
signal seems like it's coming from the waterfall itself, and that doesn't make
any sense. However, you do notice a little path that leads behind the
waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems
to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble
for a moment. Sand begins pouring into the cave! If you don't quickly figure
out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will
come in handy here. You scan a two-dimensional vertical slice of the cave above
you (your puzzle input) and discover that it is mostly air with structures made
of rock.

Your scan traces the path of each solid rock structure and reports the x,y
coordinates that form the shape of the path, where x represents distance to the
right and y represents distance down. Each path appears as a single line of
text in your scan. After the first point of each path, each point indicates the
end of a straight horizontal or vertical line to be drawn from the previous
point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9

This scan means that there are two paths of rock; the first path consists of
two straight lines, and the second path consists of three straight lines.
(Specifically, the first path consists of a line of rock from 498,4 through
498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.

Sand is produced one unit at a time, and the next unit of sand is not produced
until the previous unit of sand comes to rest. A unit of sand is large enough
to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately
below is blocked (by rock or sand), the unit of sand attempts to instead move
diagonally one step down and to the left. If that tile is blocked, the unit of
sand attempts to instead move diagonally one step down and to the right. Sand
keeps moving as long as it is able to do so, at each step trying to move down,
then down-left, then down-right. If all three possible destinations are
blocked, the unit of sand comes to rest and no longer moves, at which point the
next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply
falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.

The second unit of sand then falls straight down, lands on the first one, and
then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.

After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.

After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.

Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.

Once all 24 units of sand shown above have come to rest, all further sand flows
out the bottom, falling into the endless void. Just for fun, the path any new
sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........

Using your scan, simulate the falling sand. How many units of sand come to rest
before sand starts flowing into the abyss below?

--- Part Two ---

You realize you misread the scan. There isn't an endless void at the bottom of
the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite
horizontal line with a y coordinate equal to two plus the highest y coordinate
of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the
floor is at y=11. (This is as if your scan contained one extra rock path like
-infinity,11 -> infinity,11.) With the added floor, the example above now looks
like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->

To find somewhere safe to stand, you'll need to simulate falling sand until a
unit of sand comes to rest at 500,0, blocking the source entirely and stopping
the flow of sand into the cave. In the example above, the situation finally
looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################

Using your scan, simulate the falling sand until the source of the sand becomes
blocked. How many units of sand come to rest?
'''
import os
import sys
import time

# Local imports
from aoc2022 import AOC2022

# Color constants
RED = '\033[38;5;1m'
YELLOW = '\033[38;5;3m'
ENDC = '\033[0m'

ROCK = f'{RED}#{ENDC}'
SAND = f'{YELLOW}o{ENDC}'
AIR = '.'


class AOC2022Day14(AOC2022):
    '''
    Day 14 of Advent of Code 2022
    '''
    day = 14

    def __init__(self, example: bool = False) -> None:
        '''
        Load the cleaning assignment pairs into tuples of sets of ints
        '''
        super().__init__(example=example)

        rocks = set()

        with self.input.open() as fh:
            for line in fh:
                rock_segment = []
                for coord in line.rstrip().split(' -> '):
                    x, y = (int(item) for item in coord.split(','))
                    try:
                        prev_x, prev_y = rock_segment[-1]
                    except IndexError:
                        pass
                    else:
                        if x != prev_x:
                            start, end = sorted((x, prev_x))
                            rock_segment.extend(
                                (x_pos, y) for x_pos in
                                range(start, end + 1)
                            )
                        else:
                            start, end = sorted((y, prev_y))
                            rock_segment.extend(
                                (x, y_pos) for y_pos in
                                range(start, end + 1)
                            )
                    rock_segment.append((x, y))
                rocks.update(rock_segment)

        self.offset = min(item[0] for item in rocks)
        self.width = max(item[0] for item in rocks) - self.offset + 1
        self.bottom_row = max(item[1] for item in rocks)
        self.floor = self.bottom_row + 2
        self.drop_point = (500, 0)
        self.rocks = frozenset(rocks)
        self.grid = {}

    def reset(self) -> None:
        '''
        Reset the grid
        '''
        self.grid = {coord: ROCK for coord in self.rocks}

    def draw(self) -> None:
        '''
        Draw the grid
        '''
        for coord in list(self.grid)[-1:0:-1]:
            if self.grid[coord] == SAND:
                newest_sand = coord
                break
        else:
            newest_sand = None

        bottom = max(item[1] for item in self.grid)

        col_min = min(item[0] for item in self.grid)
        col_max = max(item[0] for item in self.grid)

        os.system('clear')
        for row in range(0, bottom + 1):
            for col in range(col_min, col_max + 1):
                coord = (col, row)
                if coord in self.grid:
                    substance = self.grid[coord]
                    if substance == SAND and coord == newest_sand:
                        substance = '*'
                    sys.stdout.write(substance)
                elif coord == self.drop_point:
                    sys.stdout.write(f'{YELLOW}+{ENDC}')
                else:
                    sys.stdout.write(AIR)
            sys.stdout.write('\n')
        sys.stdout.write('\n')
        sys.stdout.flush()

    def drop(self, part: int) -> bool:
        '''
        Drop a grain of sand
        '''
        col = self.drop_point[0]

        match part:
            case 1:
                for row in range(self.bottom_row + 1):
                    coord = (col, row)
                    if coord in self.grid:
                        if (col - 1, row) not in self.grid:
                            col -= 1
                        elif (col + 1, row) not in self.grid:
                            col += 1
                        else:
                            self.grid[(col, row - 1)] = SAND
                            break
                else:
                    return False
                return True

            case 2:
                for row in range(self.floor + 1):
                    coord = (col, row)
                    if coord in self.grid:
                        if coord == self.drop_point:
                            return False
                        if (col - 1, row) not in self.grid:
                            col -= 1
                        elif (col + 1, row) not in self.grid:
                            col += 1
                        else:
                            self.grid[(col, row - 1)] = SAND
                            break
                else:
                    self.grid[(col, self.floor - 1)] = SAND
                return True

            case _:
                raise ValueError(f'Invalid part {part!r}')

    def the_sand_must_flow(self, part: int, draw: bool = False) -> int:
        '''
        Count dropped sand grains until the end condition is reached
        '''
        # Reset the grid
        self.reset()

        count = 0
        while self.drop(part=part):
            count += 1
            if draw and (count % 100 == 0):
                self.draw()
                time.sleep(0.1)

        if draw:
            # Draw the cave one last time
            self.draw()

        return count

    def part1(self, draw: bool = False) -> int:
        '''
        Simulate dropping sand using the parameters from part 1
        '''
        return self.the_sand_must_flow(part=1, draw=draw)

    def part2(self, draw: bool = False) -> int:
        '''
        Simulate dropping sand using the parameters from part 2
        '''
        return self.the_sand_must_flow(part=2, draw=draw)

if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day14(example=True)
    aoc.validate(aoc.part1(), 24)
    aoc.validate(aoc.part2(), 93)
    # Run against actual data
    aoc = AOC2022Day14(example=False)
    aoc.run()
