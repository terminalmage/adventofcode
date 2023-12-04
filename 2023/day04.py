#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/4
'''
import functools
from collections.abc import Sequence

# Local imports
from aoc import AOC


class ScratchCard:
    '''
    Represents a single scratchcard game
    '''
    def __init__(
        self,
        card_num: int,
        winners: Sequence[int],
        picks: Sequence[int],
    ) -> None:
        '''
        Initialize the object
        '''
        self.card_num = card_num
        self.winners = frozenset(winners)
        self.picks = frozenset(picks)

    def __repr__(self) -> str:
        '''
        String representation of class instance
        '''
        return (
            f'{self.__class__.__name__}({self.card_num}, '
            f'winners={tuple(sorted(self.winners))}, '
            f'picks={tuple(sorted(self.picks))})'
        )

    @functools.cached_property
    def matches(self) -> frozenset[int]:
        '''
        Returns the set of winning picks
        '''
        return self.winners & self.picks

    @functools.cached_property
    def score(self) -> int:
        '''
        Returns the score of the game
        '''
        matches = len(self.matches)

        if matches:
            return 2 ** (matches - 1)

        return 0


class AOC2023Day4(AOC):
    '''
    Day 4 of Advent of Code 2023
    '''
    day = 4

    def __init__(self, example: bool = False) -> None:
        '''
        Read in scratch cards
        '''
        super().__init__(example=example)
        self.cards = {}
        with self.input.open() as fh:
            for line in fh:
                card_num, card_def = line.split(None, 2)[1:]
                card_num = int(card_num.rstrip(':'))
                winners, picks = card_def.split('|')

                self.cards[card_num] = ScratchCard(
                    card_num,
                    (int(item) for item in winners.strip().split()),
                    (int(item) for item in picks.strip().split()),
                )

    def part1(self) -> int:
        '''
        Return the sum of game scores
        '''
        return sum(game.score for game in self.cards.values())

    def part2(self) -> int:
        '''
        Return the total number of cards earned after playing through each of
        them once
        '''
        stacks = {card_num: 1 for card_num in self.cards}

        for card_num, card in self.cards.items():
            # As we cycle through the cards, always make sure to add its
            # winners to the stacks once for each copy of that card.
            copies = stacks[card_num]
            # This for loop will be a no-op if there are no matches
            for earned in range(card_num + 1, card_num + 1 + len(card.matches)):
                # Membership check to prevent out-of-bounds (i.e. the last
                # card can't win any subsequent cards)
                if earned in self.cards:
                    stacks[earned] += copies

        return sum(stacks.values())


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day4(example=True)
    aoc.validate(aoc.part1(), 13)
    aoc.validate(aoc.part2(), 30)
    # Run against actual data
    aoc = AOC2023Day4(example=False)
    aoc.run()
