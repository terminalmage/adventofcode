#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/10
'''
import itertools
import re
from collections.abc import Iterator

# Local imports
from aoc2022 import AOC2022


class AOC2022Day10(AOC2022):
    '''
    Day 10 of Advent of Code 2022
    '''
    day = 10

    def __init__(self, example: bool = False) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        super().__init__(example=example)

        self.deltas = []

        inst_re = re.compile(r'^(noop)|(addx) (-?\d+)$')

        with self.input.open() as fh:
            for noop, _, delta in (
                inst_re.match(line.rstrip('\n')).groups()
                for line in fh
            ):
                if noop:
                    self.deltas.append(0)
                else:
                    self.deltas.extend((0, int(delta)))

    def part1(self) -> int:
        '''
        Run through the moves given the specified number of knots. Return the
        number of distinct coordinates that the tail visits.
        '''
        def _seq() -> Iterator[int]:
            '''
            Generator to return the 20 and then every 40 after that, until
            the value exceeds the amount of cycles
            '''
            yield 20
            max_val = len(self.deltas)
            for item in itertools.count(60, 40):
                if item > max_val:
                    break
                yield item

        start = 0
        reg = 1
        total = 0

        for cycle in _seq():
            # Get the deltas for all of the cycles in this loop iteration
            deltas = self.deltas[start:cycle]
            # Deltas are applied to close the cycle, so add everything but the
            # last delta to the register
            reg += sum(deltas[:-1])
            # Increment the running total with the product of the current
            # register value and the current cycle number
            total += reg * cycle
            # Add the last delta, closing out this cycle
            reg += deltas[-1]
            # Start the next iteration's slice where we left off
            start = cycle

        return total

    def part2(self) -> str:
        '''
        Render the CRT result using the register position to represent the
        center of the sprite
        '''
        output = ''
        width = 40
        # Cols are zero-indexed, so the final col will be one less than the
        # width of the column
        eol = width - 1
        # Set the initial position of the register
        reg = 1
        # Render the result
        for cycle, delta in enumerate(self.deltas):
            col = cycle % width
            output += '#' if col in (reg - 1, reg, reg + 1) else '.'
            if col == eol:
                output += '\n'
            reg += delta
        return output


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day10(example=True)
    aoc.validate(aoc.part1(), 13140)
    aoc.validate(aoc.part2(), '''\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
''')
    # Run against actual data
    #
    # NOTE: The result for the 2nd part prints several lines to stdout, so it
    # doesn't work with the .run() function from the parent class. Therefore,
    # each part has to manually be run and the results printed to stdout.
    aoc = AOC2022Day10(example=False)
    print('Result for Day 10')
    print('-----------------')
    print(f'Answer 1: {aoc.part1()}')
    print(f'Answer 2:\n{aoc.part2()}')
