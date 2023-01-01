#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/13
'''
import itertools
import re
from collections import defaultdict

# Local imports
from aoc import AOC


class AOC2015Day13(AOC):
    '''
    Day 13 of Advent of Code 2015
    '''
    day = 13

    def load_guests(self) -> defaultdict[str, dict]:
        '''
        Load the guests from the config file
        '''
        guests = defaultdict(dict)
        happiness_re = re.compile(r'(\w+) would (gain|lose) (\d+).+ next to (\w+)')

        with self.input.open() as fh:
            for line in fh:
                name1, gain_lose, amount, name2 = happiness_re.match(line).groups()
                amount = int(amount)
                if gain_lose == 'lose':
                    amount *= -1
                guests[name1][name2] = amount

        return guests

    def calculate_happiness(self, guests, *order: str) -> int:
        '''
        Given the seating arrangement, calculate the happiness
        '''
        num_guests = len(order)
        return sum(
            guests[order[index]][order[(index + 1) % num_guests]] +
            guests[order[(index + 1) % num_guests]][order[index]]
            for index in range(num_guests)
        )

    def brute_force(self, guests: defaultdict[str, dict]) -> int:
        '''
        Try each permutation with the specified strategy
        '''
        # Table is circular, so we don't have to test every possible ordering.
        # Get the first person (the "head"), then calculate happiness levels
        # with the head in the first position and all permutations of the
        # remaining guests.
        names = list(guests)
        head = names[0]
        return max(
            self.calculate_happiness(guests, head, *others)
            for others in itertools.permutations(names[1:])
        )

    def part1(self) -> int:
        '''
        Return optimal happiness
        '''
        return self.brute_force(self.load_guests())

    def part2(self) -> int:
        '''
        Return optimal happiness with myself added to seating arrangement
        '''
        guests = self.load_guests()
        for name in list(guests):
            guests['Erik'][name] = guests[name]['Erik'] = 0
        return self.brute_force(guests)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day13(example=True)
    aoc.validate(aoc.part1(), 330)
    aoc.validate(aoc.part2(), 286)
    # Run against actual data
    aoc = AOC2015Day13(example=False)
    aoc.run()
