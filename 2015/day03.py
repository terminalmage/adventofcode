#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/3

--- Day 3: Perfectly Spherical Houses in a Vacuum ---

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and
then an elf at the North Pole calls him via radio and tells him where to move
next. Moves are always exactly one house to the north (^), south (v), east (>),
or west (<). After each move, he delivers another present to the house at his
new location.

However, the elf back at the north pole has had a little too much eggnog, and
so his directions are a little off, and Santa ends up visiting some houses more
than once. How many houses receive at least one present?

For example:

- > delivers presents to 2 houses: one at the starting location, and one to the
  east.

- ^>v< delivers presents to 4 houses in a square, including twice to the house
  at his starting/ending location.

- ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2
  houses.

--- Part Two ---

The next year, to speed up the process, Santa creates a robot version of
himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the
same starting house), then take turns moving based on instructions from the
elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

- ^v delivers presents to 3 houses, because Santa goes north, and then
  Robo-Santa goes south.

- ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back
  where they started.

- ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction
  and Robo-Santa going the other.
'''
import itertools

# Local imports
from aoc import AOC


class AOC2015Day3(AOC):
    '''
    Day 3 of Advent of Code 2015
    '''
    day = 3

    def __init__(self, example: bool = False) -> None:
        '''
        Load the directions, translating them to coordinate deltas
        '''
        super().__init__(example=example)
        deltas = {
            '^': (0, 1),
            'v': (0, -1),
            '<': (-1, 0),
            '>': (1, 0),
        }
        self.directions = tuple(
            deltas[direction] for direction in self.input.read_text().rstrip()
        )

    def part1(self) -> int:
        '''
        Return the number of houses Santa will visit
        '''
        last = (0, 0)
        houses = {last}

        for delta in self.directions:
            last = tuple(sum(x) for x in zip(last, delta))
            houses.add(last)

        return len(houses)

    def part2(self) -> int:
        '''
        Return the number of houses visited by Santa and Robo-Santa
        '''
        santa = robo_santa = (0, 0)
        houses = {santa}

        for index in itertools.count(0, 2):
            deltas = self.directions[index:index + 2]
            if not deltas:
                break
            santa = tuple(sum(x) for x in zip(santa, deltas[0]))
            houses.add(santa)
            try:
                robo_santa = tuple(sum(x) for x in zip(robo_santa, deltas[1]))
                houses.add(robo_santa)
            except IndexError:
                pass

        return len(houses)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day3(example=True)
    aoc.validate(aoc.part1(), 2)
    aoc.validate(aoc.part2(), 11)
    # Run against actual data
    aoc = AOC2015Day3(example=False)
    aoc.run()
