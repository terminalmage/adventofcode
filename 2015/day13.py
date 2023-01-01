#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/13

--- Day 13: Knights of the Dinner Table ---

In years past, the holiday feast with your family hasn't gone so well. Not
everyone gets along! This year, you resolve, will be different. You're going to
find the optimal seating arrangement and avoid all those awkward conversations.

You start by writing up a list of everyone invited and the amount their
happiness would increase or decrease if they were to find themselves sitting
next to each other person. You have a circular table that will be just big
enough to fit everyone comfortably, and so each person will have exactly two
neighbors.

For example, suppose you have only four attendees planned, and you calculate
their potential happiness as follows:

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

Then, if you seat Alice next to David, Alice would lose 2 happiness units
(because David talks so much), but David would gain 46 happiness units (because
Alice is such a good listener), for a total change of 44.

If you continue around the table, you could then seat Bob next to Alice (Bob
gains 83, Alice gains 54). Finally, seat Carol, who sits next to Bob (Carol
gains 60, Bob loses 7) and David (Carol gains 55, David gains 41). The
arrangement looks like this:

     +41 +46
+55   David    -2
Carol       Alice
+60    Bob    +54
     -7  +83

After trying every other seating arrangement in this hypothetical scenario, you
find that this one is the most optimal, with a total change in happiness of
330.

What is the total change in happiness for the optimal seating arrangement of
the actual guest list?

--- Part Two ---

In all the commotion, you realize that you forgot to seat yourself. At this
point, you're pretty apathetic toward the whole thing, and your happiness
wouldn't really go up or down regardless of who you sit next to. You assume
everyone else would be just as ambivalent about sitting next to you, too.

So, add yourself to the list, and give all happiness relationships that involve
you a score of 0.

What is the total change in happiness for the optimal seating arrangement that
actually includes yourself?
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
