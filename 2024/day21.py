#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/21
'''
import functools
import textwrap
from typing import Callable

# Local imports
from aoc import AOC, TupleMixin, XY


class AOC2024Day21(AOC, TupleMixin):
    '''
    Day 21 of Advent of Code 2024
    '''
    keypad: dict[str, XY] = {
        '7' : (0, -3), '8' : (1, -3), '9' : (2, -3),
        '4' : (0, -2), '5' : (1, -2), '6' : (2, -2),
        '1' : (0, -1), '2' : (1, -1), '3' : (2, -1),
                       '0' : (1,  0), 'A' : (2,  0),
    }

    d_pad: dict[str, XY] = {
                      '^' : (1, 0), 'A' : (2, 0),
        '<' : (0, 1), 'v' : (1, 1), '>' : (2, 1)
    }

    example_data: str = textwrap.dedent(
        '''
        029A
        980A
        179A
        456A
        379A
        '''
    )

    validate_part1: int = 126384

    # Set by post_init
    codes = None

    def post_init(self) -> None:
        '''
        Load the input into a Maze object
        '''
        self.codes: tuple[str, ...] = tuple(self.input.splitlines())

    # Using functools.cache on a class method is a very bad idea. Don't do this
    # in the real world, it will prevent your instances from getting GC'ed.
    @functools.cache  # pylint: disable=method-cache-max-size-none
    def num_presses(
        self,
        dest: XY,
        start: XY,
        pads_remaining: int,
        times: int = 1,
    ) -> int:
        '''
        Calculate the number of presses to get from one position to the next
        '''
        if pads_remaining == 0:
            return times

        # Calculate the overall XY change to get from the current position to
        # the destination.
        dx: int
        dy: int
        dx, dy = self.tuple_subtract(dest, start)

        # Determine the keys we need to press to move the calculated delta
        x_key: XY = self.d_pad['>'] if dx > 0 else self.d_pad['<']
        y_key: XY = self.d_pad['v'] if dy > 0 else self.d_pad['^']

        ret: int = 0

        press_a: Callable[[int], int] = lambda start: self.num_presses(
            dest=self.d_pad['A'],
            start=start,
            pads_remaining=pads_remaining - 1,
            times=times,
        )
        if not dx:
            # Only vertical movement on d-pad. Press the appropriate up or down
            # key the amount of times calculated above.
            ret += self.num_presses(
                dest=y_key,
                start=self.d_pad['A'],
                pads_remaining=pads_remaining - 1,
                times=abs(dy),
            )
            # Press the action key to lock in the keypress(es)
            ret += press_a(start=y_key)
        elif not dy:
            # Only horizontal movement on d-pad. Press the appropriate left or
            # right key the amount of times calculated above.
            ret += self.num_presses(
                dest=x_key,
                start=self.d_pad['A'],
                pads_remaining=pads_remaining - 1,
                times=abs(dx),
            )
            # Press the action key to lock in the keypress(es)
            ret += press_a(start=x_key)
        elif dest[0] == start[1] == 0:
            # Starting position is in the top row, and the dest is all the way
            # in the left column. In this case we want to move up/down first,
            # since moving left first would make go over the empty space.
            ret += self.num_presses(
                dest=y_key,
                start=self.d_pad['A'],
                pads_remaining=pads_remaining - 1,
                times=abs(dy),
            )
            # Now move horizontally
            ret += self.num_presses(
                dest=x_key,
                start=y_key,
                pads_remaining=pads_remaining - 1,
                times=abs(dx),
            )
            # Press the action key to lock in the keypress(es)
            ret += press_a(start=x_key)
        elif (dest[1] == start[0] == 0) or dx < 0:
            # My initial idea for this part of the if block was to account for
            # a current position in the far left column (that is, it did not
            # include the "or dx < 0". However, this resulted in an incorrect
            # number of keypresses for the example code 379A. After a while I
            # checked some other people's examples and there were a few who had
            # the same basic idea I did but added a conditional to check for
            # horizontal movement. In the end I adapted that additional
            # conditon and it produced the correct output, but I'm not gonna
            # lie, I don't understand *why* this works. It would seem to me
            # like attempting horizontal movement first if you are moving to
            # the left would be problematic if you are in a row with the empty
            # space. Perhaps it's an accident that it works and it is not a
            # good generalized solution.
            ret += self.num_presses(
                dest=x_key,
                start=self.d_pad['A'],
                pads_remaining=pads_remaining - 1,
                times=abs(dx),
            )
            # Now move vertically
            ret += self.num_presses(
                dest=y_key,
                start=x_key,
                pads_remaining=pads_remaining - 1,
                times=abs(dy),
            )
            # Press the action key to lock in the keypress(es)
            ret += press_a(start=y_key)
        else:
            # Move vertically first
            ret += self.num_presses(
                dest=y_key,
                start=self.d_pad['A'],
                pads_remaining=pads_remaining - 1,
                times=abs(dy),
            )
            # Now move horizontally
            ret += self.num_presses(
                dest=x_key,
                start=y_key,
                pads_remaining=pads_remaining - 1,
                times=abs(dx),
            )
            # Press the action key to lock in the keypress(es)
            ret += press_a(start=x_key)

        return ret

    def solve(self, keypads: int) -> int:
        '''
        Count the number of keypresses needed to enter each code using the
        specified number of keypads. The first keypad will always be the
        numeric pad, while all subsequent keypads will be directional pads.
        Thus, the num_presses function will only concern itself with d-pad
        inputs.
        '''
        return sum(
            self.num_presses(
                dest=self.keypad[code[index]],
                start=self.keypad[code[index - 1]],
                pads_remaining=keypads,
            ) * int(code[:-1])
            for code in self.codes
            for index in range(len(code))
        )

    def part1(self) -> int:
        '''
        Simulate with 3 keypads (numeric + 2 directional)
        '''
        return self.solve(keypads=3)

    def part2(self) -> int:
        '''
        Simulate with 26 keypads (numeric + 25 directional)
        '''
        return self.solve(keypads=26)


if __name__ == '__main__':
    aoc = AOC2024Day21()
    aoc.run()
