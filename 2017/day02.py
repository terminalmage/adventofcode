#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/2
'''
import itertools
import textwrap

# Local imports
from aoc import AOC

# Type hints
Numbers = tuple[tuple[int]]


class AOC2017Day2(AOC):
    '''
    Day 2 of Advent of Code 2017
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        5 1 9 5
        7 5 3
        2 4 6 8
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        5 9 2 8
        9 4 7 3
        3 8 6 5
        '''
    )

    validate_part1: int = 18
    validate_part2: int = 9

    def load_numbers(self, data: str) -> Numbers:
        '''
        Load the numbers from the input for the specified part, sorting each
        line as they are loaded.
        '''
        return tuple(
            tuple(
                sorted(int(item) for item in line.split())
                for line in data.splitlines()
            )
        )

    def part1(self) -> int:
        '''
        Return the sum of the difference between each line's max and min value
        '''
        numbers: Numbers = self.load_numbers(self.input_part1)
        return sum(group[-1] - group[0] for group in numbers)

    def part2(self) -> int:
        '''
        Return the sum of the quotients of equally divisible pairs for each
        line
        '''
        # itertools.combinations(), when invoked with a second argument of 2,
        # gives non-repeating pairs of elements of an iterable. It starts by
        # yielding the first and second item of the iterable, then the first
        # and third, etc. until all possible pairings of the first with the
        # other items have been exhausted. It then proceeds to pair the second
        # element of the iterable with the third (since first and second have
        # already been used), etc. For the iterable 'ABC' this works out to:
        #
        #   >>> list(itertools.combinations('ABC', 2))
        #   [('A', 'B'), ('A', 'C'), ('B', 'C')]
        #
        # Because we have sorted sequences of integers, we know that every pair
        # of integers yielded by itertools.combinations() will have a second
        # element that is >= the first.

        def special_pair(seq: tuple[int]) -> int:
            '''
            Find the pair of digits that are equally divisible and return the
            quotient.
            '''
            i: int
            j: int
            quotient: int
            remainder: int
            for i, j in itertools.combinations(seq, 2):
                quotient, remainder = divmod(j, i)
                if not remainder:
                    return quotient
            raise ValueError(f'There is nothing special about {seq}')

        numbers: Numbers = self.load_numbers(self.input_part2)
        return sum(special_pair(group) for group in numbers)


if __name__ == '__main__':
    aoc = AOC2017Day2()
    aoc.run()
