#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/2
'''
# Local imports
from aoc import AOC

# Typing shortcuts
Coordinate = tuple[int]
Step = tuple[str, int]


class AOC2016Day2(AOC):
    '''
    Day 2 of Advent of Code 2016
    '''
    day = 2

    def __init__(self, example: bool = False) -> None:
        '''
        Setup keypad
        '''
        super().__init__(example=example)
        self.instructions = tuple(self.input.read_text().splitlines())
        self.deltas = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1),
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
                position = (row_idx, row.index(start))
                break
        else:
            raise ValueError(f'Start point {start!r} not found in keypad')

        low = 0
        high = len(keypad) - 1
        code = ''

        for line in self.instructions:
            for step in line:
                new_position = tuple(
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
        keypad = (
            ('1', '2', '3'),
            ('4', '5', '6'),
            ('7', '8', '9'),
        )
        return self.find_code(keypad)

    def part2(self) -> str:
        '''
        Return the code derived from following the instructions
        '''
        keypad = (
            (None, None, '1', None, None),
            (None,  '2', '3',  '4', None),
            ( '5',  '6', '7',  '8',  '9'),
            (None,  'A', 'B',  'C', None),
            (None, None, 'D', None, None),
        )
        return self.find_code(keypad)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day2(example=True)
    aoc.validate(aoc.part1(), '1985')
    aoc.validate(aoc.part2(), '5DB3')
    # Run against actual data
    aoc = AOC2016Day2(example=False)
    aoc.run()
