#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/12
'''
import functools
import textwrap

# Local imports
from aoc import AOC

# Type hints
Definition = str
Groups = tuple[int, ...]
Configuration = tuple[tuple[Definition, Groups], ...]


@functools.cache
def possible_arrangements(
    substr: str,
    groups: Groups,
    partial: int = 0,
) -> int:
    '''
    Recursive function to find the possible arrangements for a given string
    (or substring), and a sequence of ints representing the size of
    non-contiguous groups of damaged springs.
    '''
    if not substr:
        # We've exhausted the string. If we have no groups remaining, this
        # counts as a valid configuration, but if we still have groups to
        # process, there is no valid combination for this configuration.
        return not groups  # NOTE: int(True) == 1, int(False) == 0

    # Prune recursion if there is no possible way to make a valid combination
    # with the remaining substring and groups
    if len(substr) < sum(groups) + len(groups) - 1 - partial:
        return 0

    ret: int = 0

    if substr[0] in '#?':
        # Assume that the current position is (or could be) part of a group of
        # damaged springs. Advance 1 position and find all valid partial
        # matches for the remaining substring.
        ret += possible_arrangements(substr[1:], groups, partial + 1)

    if substr[0] in '.?' and (
        (groups and groups[0] == partial)
        or not partial
    ):
        # Assume a "." (or "?" which could be a "."). Given the "and" clause
        # directly above, we know that one of two things are true:
        #
        # 1) The size of the current group is equal to the length of the
        #    current partial match
        # 2) There is no partial match.
        #
        # If there is currently a partial match, assume that the character at
        # the current position has ended the current group, and proceed to find
        # all possible arrangements for the remaining substring and groups.
        #
        # Otherwise, assume that the current character is part of a series of
        # contiguous dots, and continue to look for possible arrangements for
        # the current group in the remaining substring.
        if partial:
            ret += possible_arrangements(substr[1:], groups[1:])
        else:
            ret += possible_arrangements(substr[1:], groups)

    return ret


class AOC2023Day12(AOC):
    '''
    Day 12 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        ???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1
        '''
    )

    validate_part1: int = 21
    validate_part2: int = 525152

    # Set by post_init
    configurations = None

    def post_init(self) -> None:
        '''
        Load configurations from the input file
        '''
        self.configurations: tuple[Configuration] = tuple(
            (definition, tuple((int(x) for x in groups.split(','))))
            for definition, groups in (
                line.split()
                for line in self.input.splitlines()
            )
        )

    @staticmethod
    def solve(definition: Definition, groups: Groups) -> int:
        '''
        The recursive function to get the possible arrangements depends on
        dots to denote the end of a group. If a definition ends in a "#" it
        will always be miscalculated, and if it ends in a "?" it may or may not
        be miscalculated. To fix this, add an explicit "." to the definition
        before calculating the number of possible arrangements.
        '''
        return possible_arrangements(f'{definition}.', groups)

    def part1(self) -> int:
        '''
        Returns total number of possible combinations
        '''
        return sum(
            self.solve(*configuration)
            for configuration in self.configurations
        )

    def part2(self) -> int:
        '''
        Assuming the configurations were folded, "unfold" them and then return
        the total number of possible combinations.
        '''
        return sum(
            self.solve(*configuration)
            for configuration in (
                ('?'.join([config[0]] * 5), config[1] * 5)
                for config in self.configurations
            )
        )


if __name__ == '__main__':
    aoc = AOC2023Day12()
    aoc.run()
