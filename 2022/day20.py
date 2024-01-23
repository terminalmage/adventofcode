#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/20
'''
from collections import deque
from collections.abc import Sequence

# Local imports
from aoc import AOC

DEFAULT_KEY: int = 1


class Cipher:
    '''
    Implements the Grove Positioning System
    '''
    def __init__(
        self,
        data: str,
        key: int = DEFAULT_KEY,
    ) -> None:
        '''
        Load the cipher data from the filehandle
        '''
        self.data: deque[tuple[int, int]] = deque(
            enumerate(int(x) * key for x in data.splitlines())
        )

    @property
    def coordinates(self) -> int:
        '''
        Calculate the coordinates by first finding the index of the zero value,
        and then adding together the values at offset 1000, 2000, and 3000 from
        that position
        '''
        # Find the queue index of the zero value
        pointer: Sequence[tuple[int, int]] = enumerate(self.data)
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
        original_order: list[int] = list(self.data)
        for _ in range(rounds):
            item: int
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
    def load_cipher(self, key=DEFAULT_KEY) -> Cipher:
        '''
        Load the input file into a Cipher object
        '''
        return Cipher(self.input, key=key)

    def part1(self) -> int:
        '''
        Decrypt the cipher and return the coordinates
        '''
        cipher: Cipher = self.load_cipher()
        cipher.decrypt()
        return cipher.coordinates

    def part2(self) -> int:
        '''
        Decrypt the cipher (10 rounds) using the key from part 2
        '''
        cipher: Cipher = self.load_cipher(key=811589153)
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
