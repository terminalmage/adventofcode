#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/4
'''
import functools
import textwrap
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
        self.card_num: int = card_num
        self.winners: frozenset[int] = frozenset(winners)
        self.picks: frozenset[int] = frozenset(picks)

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
        matches: int = len(self.matches)

        if matches:
            return 2 ** (matches - 1)

        return 0


class AOC2023Day4(AOC):
    '''
    Day 4 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
        '''
    )

    validate_part1: int = 13
    validate_part2: int = 30

    # Set by post_init
    cards = None

    def post_init(self) -> None:
        '''
        Read in scratch cards
        '''
        self.cards: dict[int, ScratchCard] = {}
        for line in self.input.splitlines():
            card_num: int
            card_def: str
            card_num, card_def = line.split(None, 2)[1:]
            card_num = int(card_num.rstrip(':'))
            winners: str
            picks: str
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
        stacks: dict[int, int] = {card_num: 1 for card_num in self.cards}

        card_num: int
        card: ScratchCard
        for card_num, card in self.cards.items():
            # As we cycle through the cards, always make sure to add its
            # winners to the stacks once for each copy of that card.
            copies: int = stacks[card_num]
            # This for loop will be a no-op if there are no matches
            earned: int
            for earned in range(card_num + 1, card_num + 1 + len(card.matches)):
                # Membership check to prevent out-of-bounds (i.e. the last
                # card can't win any subsequent cards)
                if earned in self.cards:
                    stacks[earned] += copies

        return sum(stacks.values())


if __name__ == '__main__':
    aoc = AOC2023Day4()
    aoc.run()
