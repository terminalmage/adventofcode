#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/4
'''
# Local imports
from aoc2022 import AOC2022


class AOC2022Day4(AOC2022):
    '''
    Base class for Day 4 of Advent of Code 2022
    '''
    day = 4

    def __init__(self, example: bool = False) -> None:
        '''
        Load the cleaning assignment pairs into tuples of sets of ints
        '''
        super().__init__(example=example)
        self.assignment_pairs = []
        with self.input.open() as fh:
            for line in fh:
                self.assignment_pairs.append(
                    tuple(
                        (
                            set(range(int(begin), int(end) + 1))
                            for begin, end in [
                                section.split('-')
                                for section in line.rstrip('\n').split(',')
                            ]
                        )
                    )
                )


if __name__ == '__main__':
    aoc = AOC2022Day4()
    answer1 = sum(
        1 for pair in aoc.assignment_pairs
        if pair[0].issuperset(pair[1])
        or pair[1].issuperset(pair[0])
    )
    print(f'Answer 1 (count of entirely overlapping assignment pairs): {answer1}')
    answer2 = sum(
        1 for pair in aoc.assignment_pairs
        if pair[0].intersection(pair[1])
    )
    print(f"Answer 2 (count of pairs with overlapping sections: {answer2}")
