#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/12
'''
import textwrap

# Local imports
from aoc import AOC

Pots = frozenset[int]


class AOC2018Day12(AOC):
    '''
    Day 12 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        initial state: #..#.#..##......###...###

        ...## => #
        ..#.. => #
        .#... => #
        .#.#. => #
        .#.## => #
        .##.. => #
        .#### => #
        #.#.# => #
        #.### => #
        ##.#. => #
        ##.## => #
        ###.. => #
        ###.# => #
        ####. => #
        '''
    )

    validate_part1: int = 325

    # Set by post_init
    initial_state = None
    rules = None

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        lines: list[str] = self.input.splitlines()
        # The initial state is represented as a frozenset of integers
        # corresponding to pot numbers containing plants. This allows us to
        # easily calculate the value of a given state by summing its integers.
        self.initial_state: Pots = frozenset({
            i for i, pot in enumerate(lines[0].split()[-1])
            if pot == '#'
        })
        # Ignore rules which set a given pot to ".", because the strategy for
        # this solution is to assume "." and check to see what would be turned
        # to "#".
        self.rules: set[str] = {
            line.split()[0] for line in lines[2:]
            if line.endswith('#')
        }

    @staticmethod
    def subset(pots: Pots, index: int) -> str:
        '''
        Since we are representing pots with plants in them using integer values
        (since the solution to the puzzle is the sum of plant positions), this
        helper function returns the subset of the flowerpots starting at the
        index two the left of the specified position, and ending 2 to the
        right. The return data is a pattern of "." and "#", where "#"
        represents an empty pot and "#" represents a pot with a plant in it.
        The pattern produced by this function can then be compared against all
        the patterns to see if any of the patterns from the rules match this
        subset.
        '''
        return ''.join(
            '#' if index + offset in pots else '.'
            for offset in range(-2, 3)
        )

    def apply_rules(self, pots: Pots) -> Pots:
        '''
        Simulate one generation
        '''
        return frozenset({
            pot_num for pot_num in range(min(pots) - 2, max(pots) + 2)
            if self.subset(pots, pot_num) in self.rules
        })

    def part1(self) -> int:
        '''
        Simulate 20 generations
        '''
        pots: Pots = self.initial_state
        for _ in range(20):
            pots = self.apply_rules(pots)

        return sum(pots)

    def part2(self) -> int:
        '''
        Simulate 50,000,000,000 generations
        '''
        pots: Pots = self.initial_state
        generations: int = 50_000_000_000

        prev: int = sum(pots)
        delta: int = 0
        streak: int = 1

        # Try at most 1000 generations. Track the delta in sum between each
        # generation. We are looking for it to stabilize (i.e. for the sum to
        # grow at the same rate from generation to generation). Assume that 20
        # consecutive generations with identical deltas constitutes a
        # stabilized pattern. Once this streak is found, we can multiply the
        # remaining number of generations by that delta and add it to our
        # current value, and that will be the solution.
        for remaining in range(generations - 1, generations - 1001, -1):
            pots = self.apply_rules(pots)
            value: int = sum(pots)
            newdelta: int = value - prev
            if newdelta == delta:
                streak += 1
            else:
                streak = 1

            if streak == 20:
                return value + (remaining * delta)

            prev = value
            delta = newdelta

        raise RuntimeError('Growth did not stabilize')


if __name__ == '__main__':
    aoc = AOC2018Day12()
    aoc.run()
