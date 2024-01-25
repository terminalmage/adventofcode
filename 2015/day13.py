#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/13
'''
import itertools
import re
import textwrap
from collections import defaultdict

# Local imports
from aoc import AOC

# Type hints
Guests = defaultdict[str, dict]


class AOC2015Day13(AOC):
    '''
    Day 13 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        Alice would gain 54 happiness units by sitting next to Bob.
        Alice would lose 79 happiness units by sitting next to Carol.
        Alice would lose 2 happiness units by sitting next to David.
        Bob would gain 83 happiness units by sitting next to Alice.
        Bob would lose 7 happiness units by sitting next to Carol.
        Bob would lose 63 happiness units by sitting next to David.
        Carol would lose 62 happiness units by sitting next to Alice.
        Carol would gain 60 happiness units by sitting next to Bob.
        Carol would gain 55 happiness units by sitting next to David.
        David would gain 46 happiness units by sitting next to Alice.
        David would lose 7 happiness units by sitting next to Bob.
        David would gain 41 happiness units by sitting next to Carol.
        '''
    )

    validate_part1: int = 330
    validate_part2: int = 286

    def load_guests(self) -> defaultdict[str, dict]:
        '''
        Load the guests from the config file
        '''
        guests = defaultdict(dict)
        happiness_re = re.compile(r'(\w+) would (gain|lose) (\d+).+ next to (\w+)')

        for line in self.input.splitlines():
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
        num_guests: int = len(order)
        return sum(
            guests[order[index]][order[(index + 1) % num_guests]] +
            guests[order[(index + 1) % num_guests]][order[index]]
            for index in range(num_guests)
        )

    def brute_force(self, guests: Guests) -> int:
        '''
        Try each permutation with the specified strategy
        '''
        # Table is circular, so we don't have to test every possible ordering.
        # Get the first person (the "head"), then calculate happiness levels
        # with the head in the first position and all permutations of the
        # remaining guests.
        names: list[str] = list(guests)
        head: str = names[0]
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
        guests: Guests = self.load_guests()
        for name in list(guests):
            guests['Erik'][name] = guests[name]['Erik'] = 0
        return self.brute_force(guests)


if __name__ == '__main__':
    aoc = AOC2015Day13()
    aoc.run()
