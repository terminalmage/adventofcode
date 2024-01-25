#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/10
'''
import heapq
import math
import re
import textwrap
from collections import defaultdict, deque
from typing import Literal

# Local imports
from aoc import AOC


class AOC2016Day10(AOC):
    '''
    Day 10 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        value 5 goes to bot 2
        bot 2 gives low to bot 1 and high to bot 0
        value 3 goes to bot 1
        bot 1 gives low to output 1 and high to bot 0
        bot 0 gives low to output 2 and high to output 0
        value 2 goes to bot 2
        '''
    )

    validate_part1: int = 2

    def sort_chips(self, goal: list[int] | None = None) -> int:
        '''
        Load the initial chip values and rules, and then process bots with two
        chips according to the rules defined in the puzzle input.
        '''
        Bucket = defaultdict[list]
        Rule = tuple[str, int, str, int]

        value_re = re.compile(r'value (\d+) goes to bot (\d+)')
        action_re = re.compile(
            r'bot (\d+) gives low to (output|bot) (\d+) '
            r'and high to (output|bot) (\d+)'
        )

        buckets: dict[str, Bucket] = {
            'bot': defaultdict(list),
            'output': defaultdict(list),
        }
        rules: dict[int, Rule] = {}

        for line in self.input.splitlines():
            try:
                (
                    source, low_type, low_dest,
                    high_type, high_dest
                ) = action_re.match(line).groups()
                rules[int(source)] = (
                    low_type, int(low_dest), high_type, int(high_dest)
                )
            except AttributeError:
                chip, bot = value_re.match(line).groups()
                heapq.heappush(buckets['bot'][int(bot)], int(chip))

        # To avoid repeated searches through the buckets, we'll use a deque to
        # store bots that have two chips (and thus are ready for their rule to
        # be processed).
        dq: deque[int] = deque()

        # Add the bots that have 2 chips in their initial state to the deque
        bot: int
        chips: list[int]
        for bot, chips in buckets['bot'].items():
            if len(chips) == 2:
                dq.append(bot)

        # Type hints for the values in the while loop below
        low: int
        high: int
        DestType = Literal['bot', 'output']
        low_type: DestType
        low_dest: int
        high_type: DestType
        high_dest: int

        while dq:
            # Get the bot from the queue. Grab its high and low chip values,
            # and clear the list.
            bot: int = dq.popleft()
            low, high = buckets['bot'][bot]
            buckets['bot'][bot].clear()

            # If the current bot has the combination of chip values we're
            # looking for, then we've found the right bot
            if goal and [low, high] == goal:
                return bot

            # Get the rule for the bot so we know where to send its chips
            low_type, low_dest, high_type, high_dest = rules.pop(bot)

            for dest_type, dest_num, chip_value in (
                (low_type, low_dest, low),
                (high_type, high_dest, high),
            ):
                heapq.heappush(buckets[dest_type][dest_num], chip_value)
                if dest_type == 'bot' and len(buckets['bot'][dest_num]) == 2:
                    # This bot has received a chip and now has two chips. Add
                    # it to the deque to ensure that it is processed in a
                    # future loop iteration.
                    dq.append(dest_num)

        if goal:
            raise RuntimeError(
                f'Failed to find a bot with the chip values {goal}'
            )

        return math.prod((buckets['output'][n][0] for n in (0, 1, 2)))

    def part1(self) -> int:
        '''
        Return the bot number holding the desired chip combination
        '''
        return self.sort_chips(goal=[2, 5] if self.example else [17, 61])

    def part2(self) -> int:
        '''
        Return the product of one of the chips in the first three outputs
        '''
        return self.sort_chips()


if __name__ == '__main__':
    aoc = AOC2016Day10()
    aoc.run()
