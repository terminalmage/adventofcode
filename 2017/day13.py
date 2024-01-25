#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/13
'''
import functools
import math
import re
import textwrap
from collections import defaultdict

# Local imports
from aoc import AOC


@functools.cache
def scanner_position(ps: int, scanner_range: int) -> int:
    '''
    For the given picosecond offset and scanner range, return the position of
    the scanner.
    '''
    # Halfway through the scanner's cycle, it will be at the highest index,
    # that is the range minus 1
    halfway: int = scanner_range - 1
    # Positions repeat, so we'll work with the remainder only
    remainder: int = ps % (halfway * 2)
    # If what's left over is <= halfway through the cycle, then the current
    # position is the same as the remainder.
    if remainder <= halfway:
        return remainder
    # Otherwise, the current position is the remainder minus the halfway point.
    # For exmaple, for a range of 4, there are 6 positions, and the halfway
    # point is 3 (at which point the scanner will be at index 3, the highest
    # numbered position). One picosecond later the remainder will be 4, at
    # which point the position will be 6 - 4 = 2, i.e. index 2. Another
    # picosecond later the remainder will be 5. 6 - 5 = 1, so the scanner will
    # be at position 1. Another picosecond later ther remainder will be 0, and
    # the scanner will be back in its initial position.
    return remainder - halfway


class AOC2017Day13(AOC):
    '''
    Day 13 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        0: 3
        1: 2
        4: 4
        6: 4
        '''
    )

    validate_part1: int = 24
    validate_part2: int = 10

    def post_init(self) -> None:
        '''
        Load the puzzle input
        '''
        self.layers: dict[int, int] = dict(
            (int(i) for i in re.findall(r'\d+', line))
            for line in self.input.splitlines()
        )

    def part1(self) -> int:
        '''
        Calculate the severity value for a packet starting at t=0
        '''
        # The packet's position will be equal to the current picosecond (ps).
        ps: int
        return sum(
            ps * self.layers[ps]
            for ps in range(1, max(self.layers) + 1)
            if ps in self.layers and not scanner_position(ps, self.layers[ps])
        )

    def part2(self) -> int:
        '''
        Calculate the minimum delay to pass through the firewall without being
        detected by a scanner
        '''
        # Since the packets move 1 unit of depth per picosecond, our congruence
        # for valid delay times is:
        #
        #   depthₙ + delay ≢ 0(mod periodₙ)
        #
        # Solving for the delay, this is:
        #
        #   delay ≢ -depthₙ(mod periodₙ)
        #
        # Group together depths that share a period in a dictionary, mapping
        # periods to -depth(mod period). These values will be forbidden for
        # that period, because they represent delays at which a scanner with
        # a given depth is in the 0 position.
        # self.layers maps depths to ranges
        periods: defaultdict[int, list[int]] = defaultdict(list)
        depth: int
        range_: int
        for depth, range_ in self.layers.items():
            # At range - 1 picoseconds the scanner reaches the furthest
            # position. It takes another range - 1 seconds to return back to
            # the original position. Thus the period is 2(range - 1).
            period: int = 2 * (range_ - 1)
            # Add the result of our congruence expression to any others already
            # found for this layer's period.
            periods[period].append(-depth % period)

        # Start with 0(mod 1), i.e. divisble by 1. This congruence is
        # guaranteed to be congruent to all the others.
        delays: list[int] = [0]
        m: int = 1

        # Iterate over periods. At each step, compute the lcm between the
        # current period and all the periods that came before. As we iterate,
        # the variable "m" will be our modulo which is common to all periods
        # processed to that point.
        for period in sorted(periods):
            # Save the previous value of m for the list comprehension below
            old_m: int = m
            # Calculate the new modulo as the LCM of the periods already
            # processed, and the one currently being processed.
            m: int = math.lcm(period, m)
            # Currently, delays contains the set of valid delays (mod old_m).
            # We need to update it to contain the list of delays which are
            # valid both (mod old_m) and (mod m). To do this, for each value in
            # the delays list, add multiples of old_m until you reach the new
            # m. Only add a value to the list if it is not one of our forbidden
            # values from the periods dict, as this dict collects delay values
            # that result in the scanner being in the 0 position when reached.
            delays = [
                delay
                for d in delays
                for delay in range(d, m, old_m)
                if delay % period not in periods[period]
            ]

        # This list now contains all valid delays (mod m). The lowest one is
        # the solution.
        return min(delays)


if __name__ == '__main__':
    aoc = AOC2017Day13()
    aoc.run()
