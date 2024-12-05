#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/5
'''
import functools
import textwrap

# Local imports
from aoc import AOC

# Type hints
Rule = tuple[int, int]
Update = tuple[int, ...]
Updates = tuple[Update, ...]


class AOC2024Day5(AOC):
    '''
    Day 5 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
        '''
    )

    validate_part1: int = 143
    validate_part2: int = 123

    # Set by post_init
    rules = None
    updates = None
    sorted_updates = None

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        rules, updates = self.input.split('\n\n')
        self.rules: frozenset[Rule]= frozenset(
            tuple(int(x) for x in line.split('|'))
            for line in rules.splitlines()
        )

        self.updates: Updates = tuple(
            tuple(int(x) for x in line.split(','))
            for line in updates.splitlines()
        )
        self.sorted_updates: Updates = tuple(
            self.sort(update) for update in self.updates
        )

    def sort(self, update: Update) -> Update:
        '''
        Use functools.cmp_to_key to sort the update into the correct order. The
        sorting is based on the following assumptions:

          1. Each rule (x, y) assumes x < y
          2. Therefore, for any two numbers (x, y), if they match that rule, we
             know that x < y. Return -1 to denote x < y.
          3. There are no repeated page numbers, so the lambda will never need
             to return 0 to denote equality.
          4. If there is no matching rule, and there is no possibility of
             equality, the only other possibility is that x > y. Return 1 to
             denote x > y.
        '''
        return tuple(
            sorted(
                update,
                key=functools.cmp_to_key(
                    lambda x, y: -1 if (x, y) in self.rules else 1
                )
            )
        )

    def part1(self) -> int:
        '''
        Return the sum of the middle page numbers for each valid update
        '''
        return sum(
            x[len(x) // 2]
            for x, y in zip(self.updates, self.sorted_updates)
            if x == y
        )

    def part2(self) -> int:
        '''
        Return the sum of the middle page numbers for each invalid update
        '''
        return sum(
            y[len(y) // 2]
            for x, y in zip(self.updates, self.sorted_updates)
            if x != y
        )


if __name__ == '__main__':
    aoc = AOC2024Day5()
    aoc.run()
