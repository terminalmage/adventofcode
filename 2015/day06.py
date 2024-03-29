#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/6
'''
import re
import textwrap
from typing import Callable, Literal

# Local imports
from aoc import AOC, XY


class AOC2015Day6(AOC):
    '''
    Day 6 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        turn on 490,490 through 499,499
        turn off 495,495 through 500,500
        toggle 494,494 through 496,496
        '''
    )

    validate_part1: int = 74
    validate_part2: int = 93

    # Set by post_init
    instructions = None
    lights = None

    def post_init(self) -> None:
        '''
        Load the instructions
        '''
        instr_re: re.Pattern = re.compile(
            r'^(turn (?:on|off)|toggle) (\d+),(\d+) through (\d+),(\d+)'
        )

        self.instructions: tuple[int, str, ...] = tuple(
            [instr.group(1)] +
            [int(x) for x in instr.groups()[1:]]
            for instr in (
                instr_re.match(line) for line in self.input.splitlines()
            )
        )
        self.lights: dict[XY, Literal[0, 1]] = {}

    def set_lights(
        self,
        actions: dict[str, Callable[[int], int]],
    ) -> None:
        '''
        Given the loaded instructions, apply the specified actions to the lights
        '''
        # Reset the lights
        self.lights.clear()
        # Apply all the actions
        for action, min_x, min_y, max_x, max_y in self.instructions:
            for col in range(min_x, max_x + 1):
                for row in range(min_y, max_y + 1):
                    self.lights[(col, row)] = actions[action](self.lights.get((col, row), 0))

    def part1(self) -> int:
        '''
        Return the number of strings which are nice under Part 1's rules
        '''
        self.set_lights({
            # Bitwise OR with 1 to set bit
            'turn on': lambda state: state | 1,
            # Bitwise AND with 0 to unset bit
            'turn off': lambda state: state & 0,
            # Bitwise XOR with 1 to flip bit
            'toggle': lambda state: state ^ 1,
        })

        return sum(1 for state in self.lights.values() if state == 1)

    def part2(self) -> int:
        '''
        Return the number of strings which are nice under Part 2's rules
        '''
        self.set_lights({
            # Increase brightness by 1
            'turn on': lambda state: state + 1,
            # Decrease brightness by 1 to a minimum of 0
            'turn off': lambda state: state if state == 0 else (state - 1),
            # Increase brightness by 2
            'toggle': lambda state: state + 2,
        })
        return sum(self.lights.values())


if __name__ == '__main__':
    aoc = AOC2015Day6()
    aoc.run()
