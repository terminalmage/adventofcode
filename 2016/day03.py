#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/3
'''
import itertools
from collections.abc import Iterator, Sequence

# Local imports
from aoc import AOC

# Typing shortcuts
Sides = tuple[int, int, int]


class AOC2016Day3(AOC):
    '''
    Day 3 of Advent of Code 2016
    '''
    @property
    def horizontal_sides(self) -> Iterator[Sides]:
        '''
        Generator to produce a sequence of items from the input file
        '''
        for line in self.input.splitlines():
            yield tuple(int(x) for x in line.split())

    @property
    def vertical_sides(self) -> Iterator[Sides]:
        '''
        Generator to produce a sequence of items from the input file
        '''
        col1 = []
        col2 = []
        col3 = []

        for line in self.input.splitlines():
            n1, n2, n3 = (int(x) for x in line.rstrip().split())
            col1.append(n1)
            col2.append(n2)
            col3.append(n3)

        nums = itertools.chain.from_iterable((col1, col2, col3))

        while sides := tuple(itertools.islice(nums, 3)):
            yield sides

    @staticmethod
    def count_valid_triangles(items: Sequence[Sides]) -> int:
        '''
        Given a sequence of groups of side lengths, return the count of groups
        which make a valid triangle.
        '''
        return sum(sum(sides) > 2 * max(sides) for sides in items)

    def part1(self) -> int:
        '''
        Return the distance from the starting point
        '''
        return self.count_valid_triangles(self.horizontal_sides)

    def part2(self) -> int:
        '''
        Return the distance from the first location visited twice
        '''
        return self.count_valid_triangles(self.vertical_sides)


if __name__ == '__main__':
    aoc = AOC2016Day3()
    aoc.run()
