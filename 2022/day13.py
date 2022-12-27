#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/13

--- Day 13: Distress Signal ---

You climb the hill and again try contacting the Elves. However, you instead
receive a signal you weren't expecting: a distress signal.

Your handheld device must still not be working properly; the packets from the
distress signal got decoded out of order. You'll need to re-order the list of
received packets (your puzzle input) to decode the message.

Your list consists of pairs of packets; pairs are separated by a blank line.
You need to identify how many pairs of packets are in the right order.

For example:

[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]

Packet data consists of lists and integers. Each list starts with [, ends with
], and contains zero or more comma-separated values (either integers or other
lists). Each packet is always a list and appears on its own line.

When comparing two values, the first value is called left and the second value
is called right. Then:

- If both values are integers, the lower integer should come first. If the left
  integer is lower than the right integer, the inputs are in the right order.
  If the left integer is higher than the right integer, the inputs are not in
  the right order. Otherwise, the inputs are the same integer; continue
  checking the next part of the input.

- If both values are lists, compare the first value of each list, then the
  second value, and so on. If the left list runs out of items first, the inputs
  are in the right order. If the right list runs out of items first, the inputs
  are not in the right order. If the lists are the same length and no
  comparison makes a decision about the order, continue checking the next part
  of the input.

- If exactly one value is an integer, convert the integer to a list which
  contains that integer as its only value, then retry the comparison. For
  example, if comparing [0,0,0] and 2, convert the right value to [2] (a list
  containing 2); the result is then found by instead comparing [0,0,0] and [2].

Using these rules, you can determine which of the pairs in the example are in
the right order:

== Pair 1 ==
- Compare [1,1,3,1,1] vs [1,1,5,1,1]
  - Compare 1 vs 1
  - Compare 1 vs 1
  - Compare 3 vs 5
    - Left side is smaller, so inputs are in the right order

== Pair 2 ==
- Compare [[1],[2,3,4]] vs [[1],4]
  - Compare [1] vs [1]
    - Compare 1 vs 1
  - Compare [2,3,4] vs 4
    - Mixed types; convert right to [4] and retry comparison
    - Compare [2,3,4] vs [4]
      - Compare 2 vs 4
        - Left side is smaller, so inputs are in the right order

== Pair 3 ==
- Compare [9] vs [[8,7,6]]
  - Compare 9 vs [8,7,6]
    - Mixed types; convert left to [9] and retry comparison
    - Compare [9] vs [8,7,6]
      - Compare 9 vs 8
        - Right side is smaller, so inputs are not in the right order

== Pair 4 ==
- Compare [[4,4],4,4] vs [[4,4],4,4,4]
  - Compare [4,4] vs [4,4]
    - Compare 4 vs 4
    - Compare 4 vs 4
  - Compare 4 vs 4
  - Compare 4 vs 4
  - Left side ran out of items, so inputs are in the right order

== Pair 5 ==
- Compare [7,7,7,7] vs [7,7,7]
  - Compare 7 vs 7
  - Compare 7 vs 7
  - Compare 7 vs 7
  - Right side ran out of items, so inputs are not in the right order

== Pair 6 ==
- Compare [] vs [3]
  - Left side ran out of items, so inputs are in the right order

== Pair 7 ==
- Compare [[[]]] vs [[]]
  - Compare [[]] vs []
    - Right side ran out of items, so inputs are not in the right order

== Pair 8 ==
- Compare [1,[2,[3,[4,[5,6,7]]]],8,9] vs [1,[2,[3,[4,[5,6,0]]]],8,9]
  - Compare 1 vs 1
  - Compare [2,[3,[4,[5,6,7]]]] vs [2,[3,[4,[5,6,0]]]]
    - Compare 2 vs 2
    - Compare [3,[4,[5,6,7]]] vs [3,[4,[5,6,0]]]
      - Compare 3 vs 3
      - Compare [4,[5,6,7]] vs [4,[5,6,0]]
        - Compare 4 vs 4
        - Compare [5,6,7] vs [5,6,0]
          - Compare 5 vs 5
          - Compare 6 vs 6
          - Compare 7 vs 0
            - Right side is smaller, so inputs are not in the right order

What are the indices of the pairs that are already in the right order? (The
first pair has index 1, the second pair has index 2, and so on.) In the above
example, the pairs in the right order are 1, 2, 4, and 6; the sum of these
indices is 13.

Determine which pairs of packets are already in the right order. What is the
sum of the indices of those pairs?
'''
from __future__ import annotations
import functools
import itertools
import json
from collections.abc import Iterator, Sequence

# Local imports
from aoc import AOC

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


class AOC2022Day13(AOC):
    '''
    Day 13 of Advent of Code 2022
    '''
    day = 13

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the object
        '''
        super().__init__(example=example)
        self.packets = []

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

    def load_packets(self):
        '''
        Load the move list and translate it to coordinate deltas
        '''
        self.packets.clear()

        with self.input.open() as fh:
            self.packets.extend(
                Packet(*(segment for segment in json.loads(line)))
                for line in fh
                if line != '\n'
            )

    def part1(self) -> int:
        '''
        Compute the sum of the indicies of packets that are in the right order.
        Note that for the purposes of this exercise, the indicies are not
        zero-based (i.e. 1 is the first index).
        '''
        self.load_packets()
        return sum(index + 1 for index, pair in enumerate(self.pairs) if pair[0] < pair[1])

    def part2(self) -> int:
        '''
        Compute the product of the indicies of the divider packets
        '''
        self.load_packets()
        dividers = [Packet([2]), Packet([6])]
        self.packets.extend(dividers)
        self.packets.sort()
        return functools.reduce(
            lambda x, y: x * y,
            (self.packets.index(item) + 1 for item in dividers)
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day13(example=True)
    aoc.validate(aoc.part1(), 13)
    aoc.validate(aoc.part2(), 140)
    # Run against actual data
    aoc = AOC2022Day13(example=False)
    aoc.run()
