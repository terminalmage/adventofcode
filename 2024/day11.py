#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/11
'''
import functools
import textwrap
from collections import defaultdict, Counter

# Local imports
from aoc import AOC

# Type hints
Transformed = tuple[int, ...]


@functools.cache
def transform(stone: int) -> Transformed:
    '''
    Transforms the stone into one or more stones based on the rules defined
    in the puzzle. Results are cached to prevent re-calculation.

    NOTE: I had initially cached the result as an attempt to optimize the
    process for Part 2, before eventually realizing I needed to refactor. My
    solution for Part 2 after refactoring is fast without this optimization,
    but I'm leaving it in anyway.
    '''
    if not stone:
        return (1,)

    as_str = str(stone)
    if not len(as_str) % 2:
        middle: int = len(as_str) // 2
        return (int(as_str[:middle]), int(as_str[middle:]))

    return (stone * 2024,)


class AOC2024Day11(AOC):
    '''
    Day 11 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        125 17
        '''
    )

    validate_part1: int = 55312

    def blink(self, repeat: int) -> int:
        '''
        Return the number of stones after the specified number of blinks
        '''
        # Get initial counts of unique numbers. To start, this is done using a
        # collections.Counter instance, for conciseness. Since a Counter is a
        # dict subclass, it can be iterated over in the same way as a dict, and
        # then subsequent updated counts will be regular dict types.
        counts: Counter[int, int] = Counter(map(int, self.input.split()))

        for _ in range(repeat):
            # Allocate a dict to store the new counts for each unique number.
            # Using a defaultdict ensures that when indexed for the first time,
            # the value for a given key is 0. A bit cleaner than using the
            # following to increment the count:
            #
            #     blink_result.setdefault(transformed, 0) += current_count
            #
            blink_result: defaultdict[int] = defaultdict(int)

            number: int
            current_count: int
            transformed: Transformed
            for number, current_count in counts.items():
                # The "counts" dict will contain a mapping of the counts of
                # each number found on the stones. To simulate performing the
                # same translation on every copy of a stone with a given value,
                # we will simply increment using the current count of the
                # pre-transformation number. For example, if number=26 and
                # current_count=4, that means that there are 4 stones with the
                # number 26 on them. Each of them would generate an identical
                # translation, splitting into a 2 and a 6. So, to update the
                # counts we would need to add 4 2s and 4 6s to the tally.
                for transformed in transform(number):
                    blink_result[transformed] += current_count

            # Update the counts with the new state of the stones after the
            # blink is complete.
            counts: dict[int, int] = blink_result

        # The number of stones is the sum of all the counts
        return sum(counts.values())

    def part1(self) -> int:
        '''
        Return the number of stones after 25 blinks
        '''
        return self.blink(25)

    def part2(self) -> int:
        '''
        Return the number of stones after 75 blinks
        '''
        return self.blink(75)


if __name__ == '__main__':
    aoc = AOC2024Day11()
    aoc.run()
