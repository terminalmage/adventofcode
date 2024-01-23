#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/10
'''
import itertools
import re
import sys
from collections.abc import Iterator

# Local imports
from aoc import AOC


class AOC2022Day10(AOC):
    '''
    Day 10 of Advent of Code 2022
    '''
    def post_init(self) -> None:
        '''
        Load the move list and translate it to coordinate deltas
        '''
        self.deltas: list[int] = []

        inst_re: re.Pattern = re.compile(r'^(noop)|(addx) (-?\d+)$')

        noop: str | None
        delta: str
        for noop, _, delta in (
            inst_re.match(line).groups()
            for line in self.input.splitlines()
        ):
            if noop:
                self.deltas.append(0)
            else:
                self.deltas.extend((0, int(delta)))

    def render(self) -> None:
        '''
        Render the CRT result using the register position to represent the
        center of the sprite
        '''
        output: str = ''
        width: int = 40
        # Cols are zero-indexed, so the final col will be one less than the
        # width of the column
        eol: int = width - 1
        # Set the initial position of the register
        reg: int = 1
        # Render the result
        cycle: int
        delta: int
        for cycle, delta in enumerate(self.deltas):
            col = cycle % width
            output += '#' if col in (reg - 1, reg, reg + 1) else '.'
            if col == eol:
                output += '\n'
            reg += delta
        return output

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

        start: int = 0
        reg: int = 1
        total: int = 0

        cycle: int
        for cycle in _seq():
            # Get the deltas for all of the cycles in this loop iteration
            deltas: list[int] = self.deltas[start:cycle]
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


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day10(example=True)
    aoc.validate(aoc.part1(), 13140)
    aoc.validate(aoc.render(), '''\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
''')
    # Run against actual data
    aoc = AOC2022Day10(example=False)
    aoc.run()
    # Since the result is found within a multi-line string of stdout, write the
    # rendered result to stdout.
    sys.stdout.write(aoc.render())
