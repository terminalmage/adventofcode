#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/20
'''
import collections
from typing import TextIO

# Local imports
from aoc import AOC

DEFAULT_KEY = 1


class Cipher:
    '''
    Implements the Grove Positioning System
    '''
    def __init__(
        self,
        fh: TextIO,
        key: int = DEFAULT_KEY,
    ) -> None:
        '''
        Load the cipher data from the filehandle
        '''
        self.data = collections.deque(
            enumerate(map(lambda x: int(x) * key, fh))
        )

    @property
    def coordinates(self) -> int:
        '''
        Calculate the coordinates by first finding the index of the zero value,
        and then adding together the values at offset 1000, 2000, and 3000 from
        that position
        '''
        # Find the queue index of the zero value
        pointer = enumerate(self.data)
        while (item := next(pointer))[1][1] != 0:
            pass
        index = item[0]

        return sum(
            self.data[(index + offset) % len(self.data)][1]
            for offset in (1000, 2000, 3000)
        )

    def decrypt(self, rounds: int = 1) -> None:
        '''
        Perform decryption logic
        '''
        original_order = list(self.data)
        for _ in range(rounds):
            for item in original_order:
                # Rotate until we get to the location of this value
                self.data.rotate(-self.data.index(item))
                # Pop the value off the list, and then rotate again by that
                # amount to point the front of the queue at the location where
                # we need to move it
                self.data.rotate(-self.data.popleft()[1])
                # Place the the value in its new location
                self.data.appendleft(item)


class AOC2022Day20(AOC):
    '''
    Day 20 of Advent of Code 2022
    '''
    day = 20

    def load_cipher(self, key=DEFAULT_KEY) -> Cipher:
        '''
        Load the input file into a Cipher object
        '''
        with self.input.open() as fh:
            return Cipher(fh, key=key)

    def part1(self) -> int:
        '''
        Decrypt the cipher and return the coordinates
        '''
        cipher = self.load_cipher()
        cipher.decrypt()
        return cipher.coordinates

    def part2(self) -> int:
        '''
        Decrypt the cipher (10 rounds) using the key from part 2
        '''
        cipher = self.load_cipher(key=811589153)
        cipher.decrypt(rounds=10)
        return cipher.coordinates


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day20(example=True)
    aoc.validate(aoc.part1(), 3)
    aoc.validate(aoc.part2(), 1623178306)
    # Run against actual data
    aoc = AOC2022Day20(example=False)
    aoc.run()
