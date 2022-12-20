#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/14
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
