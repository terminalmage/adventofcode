#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/2
'''
import textwrap

# Local imports
from aoc import AOC, XY, directions

# Typing shortcuts
Step = tuple[str, int]


class AOC2016Day2(AOC):
    '''
    Day 2 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        ULL
        RRDDD
        LURDL
        UUUUD
        '''
    )

    validate_part1: str = '1985'
    validate_part2: str = '5DB3'

    deltas: dict[str, XY] = {
        'U': directions.NORTH,
        'D': directions.SOUTH,
        'L': directions.WEST,
        'R': directions.EAST,
    }

    def find_code(
        self,
        keypad: tuple[tuple[None | str]],
        start: str = '5',
    ) -> str:
        '''
        Find and return the code, using the provided instructions and a given
        keypad and start point
        '''
        if (
            len({len(row) for row in keypad}) > 1
            or len(keypad) != len(keypad[0])
        ):
            raise ValueError('Keypad must be square')


        for row_idx, row in enumerate(keypad):
            if start in row:
                position: XY = (row_idx, row.index(start))
                break
        else:
            raise ValueError(f'Start point {start!r} not found in keypad')

        low: int = 0
        high: int = len(keypad) - 1
        code: str = ''

        line: str
        for line in self.input.splitlines():
            step: str
            for step in line:
                new_position: tuple[int, ...] = tuple(
                    max(low, min(position[i] + self.deltas[step][i], high))
                    for i in range(len(position))
                )
                if keypad[new_position[0]][new_position[1]] is not None:
                    position = new_position

            code += keypad[position[0]][position[1]]

        return code

    def part1(self) -> str:
        '''
        Return the code derived from following the instructions
        '''
        # Type hints
        KeypadLine = tuple[str, str, str]

        keypad: tuple[KeypadLine, ...] = (
            ('1', '2', '3'),
            ('4', '5', '6'),
            ('7', '8', '9'),
        )
        return self.find_code(keypad)

    def part2(self) -> str:
        '''
        Return the code derived from following the instructions
        '''
        # Type hints
        Tile = str | None
        KeypadLine = tuple[Tile, Tile, Tile, Tile, Tile]

        keypad: tuple[KeypadLine, ...] = (
            (None, None, '1', None, None),
            (None,  '2', '3',  '4', None),
            ( '5',  '6', '7',  '8',  '9'),
            (None,  'A', 'B',  'C', None),
            (None, None, 'D', None, None),
        )
        return self.find_code(keypad)


if __name__ == '__main__':
    aoc = AOC2016Day2()
    aoc.run()
