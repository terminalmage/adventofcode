#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/25
'''
import textwrap
from typing import Never, Self, Type

# Local imports
from aoc import AOC


class DoorSecurity:
    '''
    Base class for Lock and Key objects
    '''
    def __init__(self, schematic: str) -> Never:
        '''
        Determines the depth of each column, storing the result in a tuple
        '''
        lines: list[str] = schematic.splitlines()
        self.rows: int = len(lines)
        self.cols: int = len(lines[0])

        self.depth: tuple[int] = tuple(
            sum(1 for row in range(self.rows) if lines[row][col] == '#')
            for col in range(self.cols)
        )

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'{self.__class__.__name__}(depth={self.depth})'

    @staticmethod
    def factory(schematic: str) -> Type:
        '''
        Return the correct instance based on the schematic
        '''
        if all(x == '#' for x in schematic.split('\n', 1)[0]):
            return Lock(schematic)
        return Key(schematic)

    def fits(self, other: Self) -> bool:
        '''
        # Returns True if the key will fit in the lock, otherwise False
        '''
        if self.__class__ is other.__class__:
            raise ValueError(
                f'Cannot compare a {self.__class__.__name__} with a '
                f'{other.__class__.__name__}, must be different types'
            )

        return all(
            first + second <= self.rows
            for first, second in zip(self.depth, other.depth)
        )


class Key(DoorSecurity):
    '''
    Represents a Key
    '''


class Lock(DoorSecurity):
    '''
    Represents a Lock
    '''


class AOC2024Day25(AOC):
    '''
    Day 25 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        #####
        .####
        .####
        .####
        .#.#.
        .#...
        .....

        #####
        ##.##
        .#.##
        ...##
        ...#.
        ...#.
        .....

        .....
        #....
        #....
        #...#
        #.#.#
        #.###
        #####

        .....
        .....
        #.#..
        ###..
        ###.#
        ###.#
        #####

        .....
        .....
        .....
        #....
        #.#..
        #.#.#
        #####
        '''
    )

    validate_part1: int = 3

    def part1(self) -> int:
        '''
        Return the number of unique Lock/Key combinations that fit without
        overlapping each other.
        '''
        locks: list[Lock] = []
        keys: list[Key] = []

        schematic: str
        item: Lock | Key
        for schematic in self.input.split('\n\n'):
            item = DoorSecurity.factory(schematic)
            if isinstance(item, Lock):
                locks.append(item)
            else:
                keys.append(item)

        return sum(lock.fits(key) for lock in locks for key in keys)


if __name__ == '__main__':
    aoc = AOC2024Day25()
    aoc.run()
