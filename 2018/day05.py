#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/5
'''
import functools
import re
import textwrap

# Local imports
from aoc import AOC


class AOC2018Day5(AOC):
    '''
    Day 5 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        dabAcCaCBAcCcaDA
        '''
    )

    validate_part1: int = 10
    validate_part2: int = 4

    @staticmethod
    def react(reacted_polymer: str, unit: str) -> str:
        '''
        Function to be used in reduce operation to simulate polymer reactions.
        As this function is repeatedly called by functools.reduce(),
        "reacted_polymer" will contain the in-progress polymer being
        constructed by functools.reduce(), while "unit" will contain the
        current unit being processed from the second argument to
        functools.reduce().

        In each call, the tail of the "reacted polymer" is compared to the the
        "unit". Consider the example polymer:

            dabAcCaCBAcCcaDA

        As functools.reduce() processes the polymer string, no "reactions" will
        occur until the "c" and "C" react. During this call, reacted_polymer will be
        "dabAc", and unit will be "C". To simulate the reaction, we will remove
        the "c" from the end of the reacted polymer, leaving "dabA". The
        following iteration of the reduce operation will call this function
        with a reacted_polymer of "dabA" and a unit of "a", leading to the "A"
        being removed. This process repeates until all units from the original
        polymer have been processed, at which point the reacted_polymer will
        contain the result after all reactions have taken place.
        '''
        try:
            if (
                reacted_polymer[-1] != unit
                and reacted_polymer[-1].lower() == unit.lower()
            ):
                # The tail of the reacted polymer reacts with the unit next to
                # it, causing the tail to be removed.
                return reacted_polymer[:-1]
        except IndexError:
            pass

        # No "reaction" occurs. The unit is added to the end of the reacted
        # polymer.
        return reacted_polymer + unit

    def do_reaction(self, polymer: str):
        '''
        Use functools.reduce to process all reactions
        '''
        return functools.reduce(self.react, polymer)

    def part1(self) -> int:
        '''
        Return the length of the polymer after all reactions have taken place
        '''
        return len(self.do_reaction(self.input))

    def part2(self) -> int:
        '''
        Return the length of the smallest polymer that can be created if all
        occurrences of a given letter (both uppercase and lowercase) are
        removed from the polymer before starting the reaction.
        '''
        # set(self.input.lower()) will produce the set of all the letters in
        # the input polymer, converted to lowercase. For each letter in that
        # set, use re.sub() to remove all lowercase and uppercase versions of
        # that letter.
        return min(
            len(
                self.do_reaction(
                    re.sub(rf'[{letter}{letter.upper()}]', '', self.input),
                )
            ) for letter in set(self.input.lower())
        )


if __name__ == '__main__':
    aoc = AOC2018Day5()
    aoc.run()
