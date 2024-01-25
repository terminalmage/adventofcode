#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/17
'''
import textwrap
from collections import defaultdict
from collections.abc import Iterator

# Local imports
from aoc import AOC


class AOC2015Day17(AOC):
    '''
    Day 17 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        20
        15
        10
        5
        5
        '''
    )

    validate_part1: int = 4
    validate_part2: int = 3

    def post_init(self) -> None:
        '''
        Load the instructions
        '''
        self.target: int = 25 if self.example else 150
        self.containers: dict[int, int] = dict(
            enumerate(int(line) for line in self.input.splitlines())
        )

    def enumerate(self, target: int | None = None) -> Iterator[tuple[int]]:
        '''
        Enumerates subsets of containers using bitwise AND.

        Given a set S, the number of possible subsets is equal to (2^len(S))-1,
        as shown below for a set of length 3:

            1) a
            2)   b
            3) a b
            4)     c
            5) a   c
            6)   b c
            7) a b c

        Subset membership for a given possible subset can thus be calculated
        using bitwise AND, given the following:

          1) Each possible subset can be represented as a binary representation
             of a number from 1 to (2^len(S)-1), i.e. 001 to 111 in our example
             set above, where a 1 means that position of the set is a member,
             and a zero means that it is not.

          2) Assigning each element of the set an index, that element is a
             member of a given subset if its index is "turned on" in the
             bitmask. For example, in combination 6 above the bitmask would be
             "110" (position 0 is turned off, while positions 1 and 2 are
             turned on). The set items "a", "b", "c" are assigned indexes 0, 1,
             and 2, respectively. Thus, "b" and "c" are in this subset.

        Mathematically, an element's membership can be calculated by performing
        a bitwise AND between the mask and 2^i, where i is the index of the
        element. If the result is zero, the element is not in the subset. Any
        other result means that the element is in the subset. In our example
        above for combination 6, we would determine set membership as follows:

        Element 0: 110 AND 001 -> 000 (not in subset)
        Element 1: 110 AND 010 -> 010 (in subset)
        Element 2: 110 AND 100 -> 100 (in subset)

        This function also has an optional argument "target", which will only
        return combinations whose sum is equal to the target.
        '''
        bitmask: int
        for bitmask in range(1, 2**len(self.containers)):
            subset: tuple[int, ...] = tuple(
                volume for index, volume in self.containers.items()
                if bitmask & 2**index
            )
            if target is None or sum(subset) == target:
                yield subset

    def part1(self) -> int:
        '''
        Calculate the number of combinations that add up to the target volume
        '''
        return sum(1 for subset in self.enumerate(target=self.target))

    def part2(self) -> int:
        '''
        Calculate the number of unique combinations with the minimum number of
        containers that add up to the target
        '''
        combo_map: defaultdict[int, int] = defaultdict(int)
        for subset in self.enumerate(target=self.target):
            combo_map[len(subset)] += 1

        return combo_map[min(combo_map)]


if __name__ == '__main__':
    aoc = AOC2015Day17()
    aoc.run()
