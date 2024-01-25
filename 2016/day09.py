#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/9
'''
import functools
import re
import textwrap

# Local imports
from aoc import AOC


@functools.cache
def decompressed_size(
    compressed: str,
    recurse: bool = False,
) -> int:
    '''
    Return the decompressed size of the data stream
    '''
    markers = re.finditer(r'\((\d+)x(\d+)\)', compressed)
    marker = None
    marker_found = False
    orig_size = len(compressed)
    ret = 0
    index = 0

    while True:
        try:
            marker = next(markers)
        except StopIteration:
            ret += orig_size - index
            break

        start, end = marker.span()

        if start < index:
            # This marker is part of the text which was consumed by the
            # previous loop iteration. Skip to the next regex match.
            continue

        # Count any bytes that come before the first marker
        if not marker_found:
            marker_found = True
            if start:
                ret += start

        length, multiplier = (int(n) for n in marker.groups())
        index = end + length

        if recurse:
            ret += decompressed_size(
                compressed[end:index] * multiplier,
                recurse=recurse,
            )
        else:
            ret += length * multiplier

    return ret


class AOC2016Day9(AOC):
    '''
    Day 9 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        X(8x2)(3x3)ABCY
        '''
    )

    validate_part1: int = 18
    validate_part2: int = 20

    def part1(self) -> int:
        '''
        Return the length of the decompressed data stream
        '''
        return decompressed_size(self.input)

    def part2(self) -> int:
        '''
        Return the length of the decompressed data stream (with recursion)
        '''
        return decompressed_size(self.input, recurse=True)


if __name__ == '__main__':
    aoc = AOC2016Day9()
    aoc.run()
