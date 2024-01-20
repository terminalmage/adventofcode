#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/10
'''
import functools
import math
import operator
from collections import deque
from collections.abc import Sequence, Generator

# Local imports
from aoc import AOC

ByteStream = Sequence[str | int]


class AOC2017Day10(AOC):
    '''
    Day 10 of Advent of Code 2017
    '''
    day = 10

    def __init__(self, example: bool = False) -> None:
        '''
        Load the puzzle input and process the stream
        '''
        super().__init__(example=example)
        self.size = 5 if self.example else 256

    @staticmethod
    def asciify(stream: ByteStream) -> Generator[int, None, None]:
        '''
        Given a sequence of characters/ints, return the ascii value of the
        string, or the int.
        '''
        for item in stream:
            try:
                yield ord(item)
            except TypeError:
                if not isinstance(item, int):
                    raise
                yield item

    def knot_hash(
        self,
        data: ByteStream,
        rounds: int = 1,
        suffix: tuple[int, ...] = (),
    ) -> list[int]:
        '''
        Perform the Knot Hash algorithm
        '''
        # Initialize the circle
        circle: deque[int] = deque(range(self.size))
        # Track total amount we rotated, so it can be reversed later
        total_rotation: int = 0
        # Skip length will increment for each length processed in each round
        skip: int = 0
        # The lengths to use
        lengths: tuple[int, ...] = tuple(self.asciify(data)) + tuple(suffix)

        for _ in range(rounds):

            length: int
            for length in lengths:
                # Reverse a chunk of the specified length
                circle.extendleft([circle.popleft() for _ in range(length)])
                # Rotate the deque to put the current positon at the beginning
                rotation: int = length + skip
                circle.rotate(-rotation)
                total_rotation += rotation
                # Increase the skip length
                skip += 1

        # Reverse the rotation to get the original front of the deque
        # back into the correct position.
        circle.rotate(total_rotation % len(circle))

        # Return the sequence of ints as a list
        return list(circle)

    def part1(self) -> int:
        '''
        Perform the Knot Hash once, with an ascending sequence of integers as
        input as described in Part 1 of the puzzle, and return the product of
        the first two items in the resulting list.
        '''
        return math.prod(
            self.knot_hash(
                data=(
                    int(x) for x in self.input.read_text().split(',')
                ),
            )[:2]
        )

    def part2(self) -> str:
        '''
        Use the more-complex instructions from Part 2 to compute the hash
        '''
        sparse_hash: list[int] = self.knot_hash(
            data=self.asciify(self.input.read_text().strip()),
            rounds=64,
            suffix=(17, 31, 73, 47, 23),
        )
        group_size: int = 16
        dense_hash: list[int] = [
            functools.reduce(operator.xor, sparse_hash[i:i+group_size])
            for i in range(0, len(sparse_hash), group_size)
        ]
        return ''.join(hex(i)[2:] for i in dense_hash)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2017Day10(example=True)
    aoc.validate(aoc.part1(), 12)
    # Run against actual data
    aoc = AOC2017Day10(example=False)
    aoc.run()
