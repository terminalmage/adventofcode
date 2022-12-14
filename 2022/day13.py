#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/13
'''
from __future__ import annotations
import functools
import itertools
import json
from collections.abc import Iterator, Sequence

# Local imports
from aoc2022 import AOC2022

LT = -1
EQ = 0
GT = 1


class Packet:
    '''
    Collection of segments
    '''
    def __init__(self, *segments: Sequence[int | list]):
        '''
        Load the segments into the data structure
        '''
        self.segments = list(segments)

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Packet({self.segments!r})'

    def __iter__(self) -> Iterator[list]:
        '''
        Iterate over segments
        '''
        return (segment for segment in self.segments)

    def __len__(self) -> Iterator[list]:
        '''
        Implement len()
        '''
        return len(self.segments)

    def __getitem__(self, index: int) -> list:
        '''
        Implement indexing
        '''
        return self.segments[index]

    def __cmp(self, seq1: list, seq2: list) -> int:
        '''
        Use zip to compare sequences until one or both run out of items
        '''
        for item1, item2 in zip(seq1, seq2):
            if isinstance(item1, int) and isinstance(item2, int):
                if item1 < item2:
                    return LT
                if item1 > item2:
                    return GT
            else:
                # Recurse into nested lists
                result = self.__cmp(
                    item1 if isinstance(item1, list) else [item1],
                    item2 if isinstance(item2, list) else [item2],
                )
                if result != EQ:
                    return result

        # One or both sequences ran out of items without finding a
        # less-than/greater-than result. Use length to determine cmp result.
        return LT if len(seq1) < len(seq2) \
            else GT if len(seq1) > len(seq2) \
            else EQ

    def __lt__(self, other: Packet) -> bool:
        '''
        Implement < operator
        '''
        return self.__cmp(self.segments, other.segments) == LT

    def __gt__(self, other: Packet) -> bool:
        '''
        Implement > operator
        '''
        return self.__cmp(self.segments, other.segments) == GT

    def __eq__(self, other: Packet) -> bool:
        '''
        Implement == operator
        '''
        return self.__cmp(self.segments, other.segments) == EQ

    def __le__(self, other: Packet) -> bool:
        '''
        Implement <= operator
        '''
        return self.__cmp(self.segments, other.segments) in (LT, EQ)

    def __ge__(self, other: Packet) -> bool:
        '''
        Implement >= operator
        '''
        return self.__cmp(self.segments, other.segments) in (GT, EQ)


class AOC2022Day13A(AOC2022):
    '''
    Part 1 of Day 13
    '''
    day = 13

    def __init__(self, example: bool = False) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        super().__init__(example=example)

        self.packets = []

        with self.input.open() as fh:
            self.packets = [
                Packet(*(segment for segment in json.loads(line)))
                for line in fh
                if line != '\n'
            ]

    @property
    def pairs(self) -> Iterator[tuple[Packet]]:
        '''
        Return packets in pairs until all packets are exhausted
        '''
        for index in itertools.count(0, 2):
            pair = tuple(self.packets[index:index + 2])
            if len(pair) != 2:
                break
            yield pair

    def run(self) -> int:
        '''
        Compute the sum of the indicies of packets that are in the right order.
        Note that for the purposes of this exercise, the indicies are not
        zero-based (i.e. 1 is the first index).
        '''
        return sum(index + 1 for index, pair in enumerate(self.pairs) if pair[0] < pair[1])


class AOC2022Day13B(AOC2022Day13A):
    '''
    Part 2 of Day 13
    '''
    def run(self) -> int:
        '''
        Compute the product of the indicies of the divider packets
        '''
        dividers = [Packet([2]), Packet([6])]
        self.packets.extend(dividers)
        self.packets.sort()
        return functools.reduce(
            lambda x, y: x * y,
            (self.packets.index(item) + 1 for item in dividers)
        )


if __name__ == '__main__':
    aoc1 = AOC2022Day13A()
    print(f'Answer 1 (sum of indicies of correctly-ordered packets): {aoc1.run()}')
    aoc2 = AOC2022Day13B()
    print(f'Answer 2 (product of indicies of divider packets): {aoc2.run()}')
