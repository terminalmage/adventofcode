#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/20
'''
# Local imports
from aoc import AOC


class AOC2016Day20(AOC):
    '''
    Day 20 of Advent of Code 2016
    '''
    day: int = 20

    def __init__(self, example: bool = False) -> None:
        '''
        Load puzzle input as a sorted sequence of IP ranges
        '''
        super().__init__(example=example)
        self.ip_ranges: tuple[tuple[int, int]] = tuple(
            sorted(
                tuple(int(ip) for ip in line.split('-'))
                for line in self.input.read_text().splitlines()
            )
        )

    def part1(self) -> int:
        '''
        Return the lowest unblocked IP
        '''
        min_unblocked: int = 0

        for ip_range in self.ip_ranges:
            if ip_range[0] <= min_unblocked <= ip_range[1]:
                min_unblocked = ip_range[1] + 1

        return min_unblocked

    def part2(self) -> int:
        '''
        Return the number of unblocked IPs
        '''
        # Convert to a list of lists so we can collapse contiguous/overlapping
        # ranges and get a sorted list of non-overlapping ranges.
        ip_ranges: list[list[int]] = [list(r) for r in self.ip_ranges]

        # Since we are modifying the list during iteration, we can't rely on
        # indexes to stay the same, so we can't just do an enumerate or iterate
        # using range(len(self.ip_ranges)). We have to check every loop
        # iteration whether or not we've reached the end, because the last
        # index will change as we collapse ranges.
        index: int = 0
        while index < len(ip_ranges) - 1:
            # Compare the max of the current range to the number before the
            # beginning of the next range.
            if ip_ranges[index][1] >= ip_ranges[index + 1][0] - 1:
                # The range at the current index is either contiuguous to or
                # overlaps with the next range. We can collapse these ranges.
                # The new max will be the highest of the maximums of both this
                # range and the next.
                ip_ranges[index][1] = max(
                    ip_ranges[i][1] for i in (index, index + 1)
                )
                # Since we've collapsed index + 1, it is now redundant and can
                # be removed.
                ip_ranges.pop(index + 1)
            else:
                # We've found a gap in blocked IPs. Increment the index and
                # continue to look for collapsible ranges.
                index += 1

        # Max theoretical number of unblocked IPs is 2^32
        unblocked: int = 10 if self.example else 2 ** 32

        # Subtract the total number of IPs in each blocked range
        ip_range: list[int]
        for ip_range in ip_ranges:
            unblocked -= ip_range[1] - ip_range[0] + 1

        # What is left over is the number of unblocked IPs
        return unblocked


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day20(example=True)
    aoc.validate(aoc.part1(), 3)
    aoc.validate(aoc.part2(), 2)
    # Run against actual data
    aoc = AOC2016Day20(example=False)
    aoc.run()