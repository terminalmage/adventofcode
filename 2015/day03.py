#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/3
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
