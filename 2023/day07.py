#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/7
'''
import collections
import textwrap

# Local imports
from aoc import AOC


class AOC2023Day7(AOC):
    '''
    Day 7 of Advent of Code 2023

    '''
    example_data: str = textwrap.dedent(
        '''
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        '''
    )

    validate_part1: int = 6440
    validate_part2: int = 5905

    def post_init(self) -> None:
        '''
        Load hands from input file
        '''
        self.hands: list[str] = self.input.splitlines()

    @staticmethod
    def key_func(hand: str, joker: bool = False) -> list[int]:
        '''
        Key function for a single hand of Camel Cards

        The hand types can be represented as a descendingly-ordered sequence of
        card frequencies (that is, the amount of an arbitrary card). For
        example:

        - Five of a kind: [5]
        - Four of a kind: [4, 1]        # 4 of some card, 1 of another
        - Full house: [3, 2]            # 3 of some card, 2 of another
        - Three of a kind: [3, 1, 1]    # 3 of one card, 1 of a 2nd, 1 of a 3rd
        - Two pair: [2, 2, 1]           # etc., etc., etc.
        - One pair: [2, 1, 1, 1]
        - High card: [1, 1, 1, 1, 1]

        These hand types also happen to be in sequence sort order!

        >>> [5] > [4, 1] > [3, 2] > [3, 1, 1] > [2, 2, 1] > [2, 1, 1, 1] > [1, 1, 1, 1, 1]
        True

        Using this information, a key function can be written to represent a
        hand as the sequence of card frequencies, followed by the the value of
        each card in the hand. Card values run from 0 -> 12, with 0 being
        assigned to a 2, and 12 being assigned to an ace (A). Considering the
        rank of hands from the example data, note that the hand type + the 5
        card values produces a list of ints which is sequence sort order:

        - QQQJA: [3, 1, 1, 10, 10, 10, 9, 12]
        - T55J5: [3, 1, 1, 8, 5, 5, 9, 4]
        - KK677: [2, 2, 1, 11, 11, 5, 6, 6]
        - KTJJT: [2, 2, 1, 11, 8, 9, 9, 8]
        - 32T3K: [2, 1, 1, 1, 1, 0, 8, 1, 11]

        For Part 2, taking jokers into account, you can simply exclude them
        from the card frequencies, and add the joker count to the most-common
        count to get the best possible hand result. Consider the case where you
        have 1 joker. Your possible frequencies for non-joker cards are:

        - [4]
        - [3, 1]
        - [2, 2]
        - [2, 1, 1]
        - [1, 1, 1, 1]

        In every case, adding your 1 joker to the most-common card frequency
        (i.e. the first element of the sequence) gives the best possible hand
        type for that combination of cards.

        Let's try 2 jokers. Here are your possible card frequencies for
        non-joker cards:

        - [3]
        - [2, 1]
        - [1, 1, 1]

        In every case, adding 2 to the first element of the sequence gives the
        best possible hand type for that combination of cards.

        To round out the sort key for the hand, do exactly the same as Part 1,
        only with the revised value order (J=0, 2=1, ..., T=9, Q=10, K=11,
        A=12). Consider the rank order of the example hands for Part 2, adding
        the card values once again results in a list of ints that is in
        sequence sort order:

        - KTJJT: [4, 1, 11, 9, 1, 1, 9]
        - QQQJA: [4, 1, 10, 10, 10, 1, 12]
        - T55J5: [4, 1, 9, 4, 4, 1, 4]
        - KK677: [2, 2, 1, 11, 11, 5, 6, 6]
        - 32T3K: [2, 1, 1, 1, 2, 1, 9, 2, 11]

        '''
        if joker:
            card_rank: str = 'J23456789TQKA'
            # A hand of all jokers would still be a 5-of-a-kind, so there would
            # be no "partial" hand in that case.
            partial: str = hand.replace('J', '') if hand != 'JJJJJ' else hand
            # Get the spread of card frequencies, ordered descendingly
            key: list[int] = sorted(
                collections.Counter(partial).values(), reverse=True
            )
            # Add the joker count to the most common card count (unless the
            # hand was all jokers)
            key[0] += len(hand) - len(partial)
        else:
            card_rank: str = '23456789TJQKA'
            # Get the spread of card frequencies, ordered descendingly
            key: list[int] = sorted(
                collections.Counter(hand).values(), reverse=True
            )

        # Add integers representing the value of each card in the hand
        key.extend(map(card_rank.index, hand))
        return key

    def calculate_winnings(self, joker: bool = False) -> int:
        '''
        Returns the sum of each hand's winnings
        '''
        return sum(
            rank * int(bid)
            for rank, (hand, bid) in enumerate(
                sorted(
                    (line.split() for line in self.hands),
                    key=lambda h: self.key_func(h[0], joker=joker)
                ),
                1
            )
        )

    def part1(self) -> int:
        '''
        Return the sum of winnings
        '''
        return self.calculate_winnings()

    def part2(self) -> int:
        '''
        Return the sum of winnings, assuming J cards are jokers
        '''
        return self.calculate_winnings(joker=True)


if __name__ == '__main__':
    aoc = AOC2023Day7()
    aoc.run()
