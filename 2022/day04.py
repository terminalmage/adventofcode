#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/4
'''
# Local imports
from aoc import AOC

# Type hints
Assignment = set[int]
AssignmentPair = tuple[Assignment, Assignment]


class AOC2022Day4(AOC):
    '''
    Day 4 of Advent of Code 2022
    '''
    def post_init(self) -> None:
        '''
        Load the cleaning assignment pairs into tuples of sets of ints
        '''
        self.assignment_pairs: list[AssignmentPair] = []
        for line in self.input.splitlines():
            self.assignment_pairs.append(
                tuple(
                    (
                        set(range(int(begin), int(end) + 1))
                        for begin, end in [
                            section.split('-')
                            for section in line.split(',')
                        ]
                    )
                )
            )

    def part1(self) -> int:
        '''
        Calculate the count of entirely overlapping assignment pairs
        '''
        return sum(
            1 for pair in aoc.assignment_pairs
            if pair[0].issuperset(pair[1])
            or pair[1].issuperset(pair[0])
        )

    def part2(self) -> int:
        '''
        Calculate the count of pairs with overlapping sections
        '''
        return sum(
            1 for pair in aoc.assignment_pairs
            if pair[0].intersection(pair[1])
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day4(example=True)
    aoc.validate(aoc.part1(), 2)
    aoc.validate(aoc.part2(), 4)
    # Run against actual data
    aoc = AOC2022Day4(example=False)
    aoc.run()
