#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/6
'''
import math
from dataclasses import dataclass

# Local imports
from aoc import AOC


@dataclass
class Race:
    '''
    Represents a single race
    '''
    time: int
    distance: int

    @property
    def bounds(self) -> tuple[int]:
        '''
        Calculate the lower and upper bounds of button-press wait time that
        beat the target time.

        Distance can be represented using the following equation:

            distance = (time - wait) * wait

        Or more concisely:

            d = tw - w²

        This can be re-arranged to be represented as a quadratic equation in
        the format ax² + bx + c = 0, like so:

            d = tw - w²
            w² + d = tw         # move w² to left via addition
            w² - tw + d = 0     # move tw to left via subtraction

        After rewriting this as a quadratic equation, the result is:

            w² - tw + d = 0

        To solve for w, use the square root method:

            x = (-b +/- sqrt(b² - 4ac)) / 2a

        Using our variable names, this would be:

            w = (-(-t) +/- sqrt(t² - 4 * 1 * d)) / (2 * 1)

        There are a couple of simplifications we can make. First, since w² has
        no multiplier, a equals 1. We can cancel it out because multplying and
        dividing by 1 is a no-op. Secondly, since t is negative, making it
        negative cancels out. Thus, our equation can be simplified further as:

            w = (t +/- sqrt(t² - 4d)) / 2
        '''
        # First, calculate sqrt(t² - 4d)
        try:
            delta = math.sqrt(self.time**2 - (4 * self.distance))
        except ValueError as exc:
            raise ValueError('No possible winning solution') from exc

        # Calculate lower and upper bounds. For the lower bound, subtract the
        # delta and divide by 2, and for the upper bound, add the delta and
        # divide by 2.
        #
        # We want to beat the record, so we'll need to add 1 to the lower
        # bound, and subtract 1 from the upper bound (holding too long will
        # result in falling short of the record). Finally, floor and ceiling
        # functions are used to get the nearest integer in both directions.
        lower = math.floor(((self.time - delta) / 2) + 1)
        upper = math.ceil(((self.time + delta) / 2) - 1)

        return lower, upper

    @property
    def winners(self) -> int:
        '''
        Return the number of winning combinations
        '''
        lower, upper = self.bounds
        return upper - lower + 1


class AOC2023Day6(AOC):
    '''
    Day 6 of Advent of Code 2023
    '''
    day = 6

    def __init__(self, example: bool = False) -> None:
        '''
        Load race data
        '''
        super().__init__(example=example)
        self.times, self.distances = (
            line.split(None, 1)[-1]
            for line in self.input.read_text().splitlines()
        )

    def part1(self) -> int:
        '''
        Return the product of the number of solutions for each race
        '''
        return math.prod(
            race.winners for race in (
                Race(*x) for x in zip(
                    (int(y) for y in self.times.split()),
                    (int(z) for z in self.distances.split()),
                )
            )
        )

    def part2(self) -> int:
        '''
        Assuming that the times and distances are single integers (ignoring
        spaces), calculate the number of winners from the single race specified
        by the input data.
        '''
        return Race(
            time=int(self.times.replace(' ', '')),
            distance=int(self.distances.replace(' ', '')),
        ).winners


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day6(example=True)
    aoc.validate(aoc.part1(), 288)
    aoc.validate(aoc.part2(), 71503)
    # Run against actual data
    aoc = AOC2023Day6(example=False)
    aoc.run()
