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

ROUNDS: int = 64
SUFFIX: tuple[int, ...] = (17, 31, 73, 47, 23)
LOOP_SIZE: int = 256

# Type hints
ByteStream = Sequence[str | int]


def sparse_hash(
    data: ByteStream,
    rounds: int = ROUNDS,
    suffix: tuple[int, ...] = SUFFIX,
    loop_size: int = LOOP_SIZE,
) -> list[int]:
    '''
    Calculate the space
    '''
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

    # Initialize the loop
    loop: deque[int] = deque(range(loop_size))
    # Track total amount we rotated, so it can be reversed later
    total_rotation: int = 0
    # Skip length will increment for each length processed in each round
    skip: int = 0
    # The data stream combined with the suffix will provide the lengths used in
    # the transformations performed below
    lengths: tuple[int, ...] = tuple(asciify(data)) + tuple(suffix)

    for _ in range(rounds):

        length: int
        for length in lengths:
            # Reverse a chunk of the specified length
            loop.extendleft([loop.popleft() for _ in range(length)])
            # Rotate the deque to put the current positon at the beginning
            rotation: int = length + skip
            loop.rotate(-rotation)
            total_rotation += rotation
            # Increase the skip length
            skip += 1

    # Reverse the rotation to get the original front of the deque
    # back into position.
    loop.rotate(total_rotation % len(loop))

    # Return the calculated sparse hash
    return list(loop)


def knot_hash(
    data: ByteStream,
    rounds: int = ROUNDS,
    suffix: tuple[int, ...] = SUFFIX,
    loop_size: int = LOOP_SIZE,
) -> None:
    '''
    Implement the knot_hash
    '''
    sparse: list[int] = sparse_hash(
        data=data,
        rounds=rounds,
        suffix=suffix,
        loop_size=loop_size,
    )

    group_size: int = 16
    dense: list[int] = [
        functools.reduce(operator.xor, sparse[i:i+group_size])
        for i in range(0, len(sparse), group_size)
    ]

    return ''.join(hex(i)[2:].zfill(2) for i in dense)


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

    def knot_hash(
        self,
        data: ByteStream,
        rounds: int = 64,
        suffix: tuple[int, ...] = (17, 31, 73, 47, 23),
        size: int = 256,
    ) -> list[int]:
        '''
        Perform the Knot Hash algorithm
        '''

    def part1(self) -> int:
        '''
        Perform the Knot Hash once, with an ascending sequence of integers as
        input as described in Part 1 of the puzzle, and return the product of
        the first two items in the resulting list.
        '''
        return math.prod(
            sparse_hash(
                data=(
                    int(x) for x in self.input.read_text().split(',')
                ),
                rounds=1,
                suffix=(),
                loop_size=self.size,
            )[:2]
        )

    def part2(self) -> str:
        '''
        Use the more-complex instructions from Part 2 to compute the hash
        '''
        return knot_hash(self.input.read_text().strip())


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2017Day10(example=True)
    aoc.validate(aoc.part1(), 12)
    # Run against actual data
    aoc = AOC2017Day10(example=False)
    aoc.run()
