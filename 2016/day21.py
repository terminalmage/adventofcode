#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/21
'''
from typing import Literal

# Local imports
from aoc import AOC

# Typing shortcuts
Chars = list[str]   # A list of single characters
Direction = Literal['left', 'right']


class AOC2016Day21(AOC):
    '''
    Day 21 of Advent of Code 2016
    '''
    day: int = 21

    def __init__(self, example: bool = False) -> None:
        '''
        Load puzzle input as a sorted sequence of IP ranges
        '''
        super().__init__(example=example)
        self.steps: tuple[str] = tuple(self.input.read_text().splitlines())

    @staticmethod
    def rotate(
        chars: Chars,
        direction: Direction,
        index: int,
    ) -> None:
        '''
        Rotate the sequence of characters by the specified amount of
        characters, in the specified direction.
        '''
        index = index % len(chars)
        match direction:
            case 'left':
                pass
            case 'right':
                # A right rotation is just a negative left rotation
                index = -index
            case _:
                raise ValueError(f'Invalid direction {direction!r}')

        # Get elements up to the index
        detached = chars[:index]
        # Remove those elements from the original list
        del chars[:index]
        # Append the detached elements to the end of list
        chars += detached

    @staticmethod
    def move(
        chars: Chars,
        x: int,
        y: int,
    ) -> None:
        '''
        Move the character at position x to position y.
        '''
        chars.insert(y, chars.pop(x))

    @staticmethod
    def reverse(
        chars: Chars,
        start: int,
        end: int,
    ) -> None:
        '''
        Modify the characters in-place, with the characters from start to end
        (inclusive) reversed.
        '''
        # Get the characters before start of reversed portion
        before: Chars = chars[:start]
        # Get the characters after end of reversed portion
        after: Chars = chars[end + 1:]
        # Get the characters from start to end position, in reverse order.
        # Since # the end of a slice is exclusive of the slice, reduce the end
        # of the slice by 1. however, if the start is 0, doing so will result
        # in an empty slice. So if the start is 0, the end of the slice will be
        # None (i.e. beginning of string).
        middle = chars[end:(start - 1) if start else None:-1]
        chars[:] = before + middle + after
        del before, middle, after

    @staticmethod
    def swap(
        chars: Chars,
        x: int | str,
        y: int | str,
    ) -> None:
        '''
        Modify the characters in-place, with the characters from start to end
        (inclusive) reversed.
        '''
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            x = chars.index(x)
            y = chars.index(y)

        new_x: str = chars[y]
        new_y: str = chars[x]
        chars[x] = new_x
        chars[y] = new_y

    def part1(self) -> str:
        '''
        Return the scrambled password
        '''
        scrambled: Chars = list('abcde' if self.example else 'abcdefgh')

        x: int | str
        y: int | str

        for step in self.steps:
            match step.split():
                case [
                    'swap', 'position' | 'letter', x,
                    'with', 'position' | 'letter', y
                ]:
                    self.swap(scrambled, x, y)

                case [
                    'rotate', ('right' | 'left') as direction,
                    x, ('step' | 'steps')
                ]:
                    self.rotate(scrambled, direction, int(x))

                case [
                    'rotate', 'based', 'on', 'position',
                    'of', 'letter', x
                ]:
                    shift: int = scrambled.index(x) + 1
                    if shift >= 5:
                        shift += 1
                    self.rotate(scrambled, 'right', shift)

                case ['reverse', 'positions', x, "through", y]:
                    self.reverse(scrambled, int(x), int(y))

                case ['move', 'position', x, 'to', 'position', y]:
                    self.move(scrambled, int(x), int(y))

                case _:
                    raise ValueError(f'Unsupported step: {step!r}')

        return ''.join(scrambled)

    def part2(self) -> str:
        '''
        Return the unscrambled password
        '''
        unscrambled: Chars = list('fbgdceah')

        x: int | str
        y: int | str

        for step in reversed(self.steps):
            match step.split():
                case [
                    'swap', 'position' | 'letter', x,
                    'with', 'position' | 'letter', y
                ]:
                    self.swap(unscrambled, x, y)

                case [
                    'rotate', ('right' | 'left') as direction,
                    x, 'step' | 'steps'
                ]:
                    self.rotate(
                        unscrambled,
                        'left' if direction == 'right' else 'right',
                        int(x),
                    )

                case [
                    'rotate', 'based', 'on', 'position',
                    'of', 'letter', x
                ]:
                    # For passwords of length 8, the scrambled position is
                    # unique (i.e. there are no repeated scrambled positions
                    # for original positions from 0-7), and the positions
                    # follow a pattern; the left shift needed to return to the
                    # original pre-scramble position is equal to: p + f(p) / 2,
                    # where p is the scrambled position, and f(p) is an offset
                    # (1 when p is odd, and 10 when p is even). This holds true
                    # for all cases except 0. A scrambled position of 0 (the
                    # beginning of the string) corresponds to a pre-scramble
                    # position at the _end_ of the string (7). Taking an
                    # original pre-scramble index of 7, and adding 1, plus an
                    # extra 1 because 7 >= 4, results in a rightward shift of
                    # 9, which is equivalent to a rightward shift of 1 since
                    # the length is 8. A rightward shift of one from the end of
                    # the string wraps around to the front of the string. So,
                    # reversing a scrambled position of 1 can be done by
                    # left-shifting by 1, which will wrap back around to the
                    # end.
                    shift: int = unscrambled.index(x)
                    if not shift:
                        shift = 1
                    else:
                        shift = (shift + (1 if (shift % 2) else 10)) // 2

                    self.rotate(unscrambled, 'left', shift)

                case ['reverse', 'positions', x, "through", y]:
                    self.reverse(unscrambled, int(x), int(y))

                case ['move', 'position', x, 'to', 'position', y]:
                    self.move(unscrambled, int(y), int(x))

                case _:
                    raise ValueError(f'Unsupported step: {step!r}')

        return ''.join(unscrambled)

if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day21(example=True)
    aoc.validate(aoc.part1(), 'decab')
    # Run against actual data
    aoc = AOC2016Day21(example=False)
    aoc.run()
