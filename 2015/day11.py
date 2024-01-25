#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/11
'''
from __future__ import annotations
import copy
import itertools
import string
from collections.abc import Sequence

# Local imports
from aoc import AOC

ORDS = dict(enumerate(string.ascii_lowercase))
CHARS = {y: x for x, y in ORDS.items()}
VERBOTEN_ORDS = frozenset(ord(x) for x in ('i', 'o', 'l'))


class Password:
    '''
    Implement the new Security-Elf's password policy
    '''
    length = 8

    def __init__(
        self,
        init: Sequence[str | int] | Password,
        strict: bool = False,
    ) -> None:
        '''
        Load the initial password
        '''
        # Allow deepcopy to work
        if isinstance(init, Password):
            self.chars = copy.deepcopy(init.chars)
            return

        self.chars = []

        ord_a = ord('a')
        for item in init:
            try:
                item_ord = ord(item) - ord_a
            except TypeError:
                # Assume integer input
                item_ord = item
            try:
                if item_ord not in ORDS:
                    raise ValueError(
                        f'Invalid character/ordinal {item!r} in password'
                    )
            except TypeError as exc:
                raise TypeError(
                    'Invalid password input, must be a sequence of '
                    'lowercase ascii characters/ordinals'
                ) from exc
            self.chars.append(item_ord)
            if len(self.chars) > self.length:
                raise ValueError('Password too long')

        if len(self.chars) < self.length:
            raise ValueError('Password too short')

        while True:
            try:
                self.__validate(self.chars)
                break
            except ValueError:
                if strict:
                    raise
                self.increment(rounds=1, in_place=True)

    def __validate(self, chars: list[int]) -> None:
        '''
        Validate the password according to the new Security-Elf's rules.
        Returns nothing if valid, otherwise raises ValueError.
        '''
        for item in chars:
            if item in VERBOTEN_ORDS:
                raise ValueError(f'Invalid character {item!r}')

        # Check for increasing straight of at least three characters. Since
        # characters are stored as a list of ints, we can just check for
        # sequentially-incrementing integers.
        for index in range(self.length - 3):
            seq = chars[index:index + 3]
            if seq == [seq[0], seq[0] + 1, seq[0] + 2]:
                break
        else:
            raise ValueError('Incrementing sequence of letters not found')

        # Look for multiple different non-overlapping pairs of repeatable
        # characters. For the first pair, stop looking if pair1_index reaches
        # length - 3, as it would be impossible to find two

        error_msg = (
            'Must contain multiple different non-overlapping pairs of '
            'repeated characters'
        )
        for pair1_index in range(self.length - 3):
            if chars[pair1_index:pair1_index + 2] == 2 * [chars[pair1_index]]:
                pair_ord = chars[pair1_index]
                break
        else:
            raise ValueError(error_msg)

        for pair2_index in range(pair1_index + 2, self.length):
            if chars[pair2_index] == pair_ord:
                # Current index points to the same character from the first
                # overlapping pair we detected. Skip this character and look at
                # the next one.
                continue
            if chars[pair2_index:pair2_index + 2] == 2 * [chars[pair2_index]]:
                break
        else:
            raise ValueError(error_msg)

    def __str__(self) -> str:
        '''
        Represent the internal sequence of ints as a string
        '''
        return ''.join(ORDS[x] for x in self.chars)

    def __repr__(self) -> str:
        '''
        Define the repr() output
        '''
        return f'Password({str(self)!r})'

    def increment(
        self,
        rounds: int = 1,
        in_place: bool = False,
    ) -> Password:
        '''
        Increment the password a specific number of times
        '''
        def _increment(chars: list[int]) -> None:
            '''
            Increment the values in the list of ints until they pass the
            validation criteria.
            '''
            while True:
                for index in itertools.count(-1, -1):
                    try:
                        chars[index] = (chars[index] + 1) % len(string.ascii_lowercase)
                        if chars[index] != 0:
                            # Stop incrementing if this column didn't roll over
                            break
                    except IndexError as exc:
                        raise OverflowError(
                            f'Password {self} cannot be incremented further'
                        ) from exc
                try:
                    self.__validate(chars)
                except ValueError:
                    continue
                # New password has successfully validated
                break

        chars = self.chars if in_place else copy.deepcopy(self.chars)

        for _ in range(rounds):
            _increment(chars)

        return self if in_place else Password(chars)


class AOC2015Day11(AOC):
    '''
    Day 11 of Advent of Code 2015
    '''
    def part1(self) -> str:
        '''
        Return next valid password, starting from the puzzle input
        '''
        return str(Password(self.input))

    def part2(self) -> int:
        '''
        Return result of incrementing the password from Part 1
        '''
        return str(Password(self.part1()).increment())


if __name__ == '__main__':
    aoc = AOC2015Day11()
    aoc.run()
