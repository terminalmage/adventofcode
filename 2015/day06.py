#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/6

--- Day 6: Probably a Fire Hazard ---

Because your neighbors keep defeating you in the holiday house decorating
contest year after year, you've decided to deploy one million lights in a
1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed
you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at
each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include
whether to turn on, turn off, or toggle various inclusive ranges given as
coordinate pairs. Each coordinate pair represents opposite corners of a
rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers
to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by
doing the instructions Santa sent you in order.

For example:

- turn on 0,0 through 999,999 would turn on (or leave on) every light.

- toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning
  off the ones that were on, and turning on the ones that were off.

- turn off 499,499 through 500,500 would turn off (or leave off) the middle
  four lights.

After following the instructions, how many lights are lit?

--- Part Two ---

You just finish implementing your winning light pattern when you realize you
mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each
light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of
those lights by 1.

The phrase turn off actually means that you should decrease the brightness of
those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of
those lights by 2.

What is the total brightness of all lights combined after following Santa's
instructions?

For example:

- turn on 0,0 through 0,0 would increase the total brightness by 1.

- toggle 0,0 through 999,999 would increase the total brightness by 2000000.
'''
import re
from typing import Callable

# Local imports
from aoc import AOC


class AOC2015Day6(AOC):
    '''
    Day 6 of Advent of Code 2015
    '''
    day = 6

    def __init__(self, example: bool = False) -> None:
        '''
        Load the instructions
        '''
        super().__init__(example=example)

        instr_re = re.compile(
            r'^(turn (?:on|off)|toggle) (\d+),(\d+) through (\d+),(\d+)'
        )

        with self.input.open() as fh:
            self.instructions = tuple(
                [instr.group(1)] +
                [int(x) for x in instr.groups()[1:]]
                for instr in (
                    instr_re.match(line) for line in fh
                )
            )
        self.lights = {}

    def reset(self):
        '''
        Reset all lights to their initial state
        '''
        self.lights.clear()

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
    # Run against test data
    aoc = AOC2015Day6(example=True)
    aoc.validate(aoc.part1(), 74)
    aoc.validate(aoc.part2(), 93)
    # Run against actual data
    aoc = AOC2015Day6(example=False)
    aoc.run()
