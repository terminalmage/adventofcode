#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/2
'''
import itertools
import textwrap

# Local imports
from aoc import AOC

# Type hints
Report = tuple[int, ...]
Reports = tuple[Report, ...]


class AOC2024Day2(AOC):
    '''
    Day 2 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
        '''
    )

    validate_part1: int = 2
    validate_part2: int = 4

    # Set by post_init
    reports = None

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.reports: Reports = tuple(
            tuple(int(x) for x in line.split())
            for line in self.input.splitlines()
        )

    @staticmethod
    def is_safe(report: Report) -> bool:
        '''
        Returns True if the report is safe, otherwise False
        '''
        # Check first two items, exit early if the delta is not within the
        # acceptable range.
        if not 1 <= abs(report[1] - report[0]) <= 3:
            return False
        # Whether or not the sequence is ascending
        ascending: bool = report[1] > report[0]

        # Start at the third item, and check if the sequence parameters still
        # hold for the remaining values
        prev: int = report[1]
        for item in itertools.islice(report, 2, None):
            delta: int = item - prev
            if not 1 <= abs(delta) <= 3:
                return False
            if not (delta > 0) == ascending:
                return False
            prev = item
        return True

    def part1(self) -> int:
        '''
        Return the number of "safe" reports
        '''
        return sum(self.is_safe(report) for report in self.reports)

    def part2(self) -> int:
        '''
        Return the number of safe reports if removing a single item from a
        report will make it "safe".

        This relies heavily on lazy evaluation. That is, we don't try
        evaluating with single items removed from a report if it was found to
        be safe by the criteria from Part 1. Additionally, the use of any()
        ensures that we stop checking potential alternate reports once we find
        the first case where removing a single item makes the report safe.
        '''
        return sum(
            self.is_safe(report)
            or any(
                self.is_safe(report[:n] + report[n + 1:])
                for n in range(len(report))
            )
            for report in self.reports
        )


if __name__ == '__main__':
    aoc = AOC2024Day2()
    aoc.run()
