#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/12
'''
import json
import textwrap
from collections.abc import Iterator
from typing import Any

# Local imports
from aoc import AOC


class AOC2015Day12(AOC):
    '''
    Day 12 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        {"a":2,"b":4,"c":[3,"red",[[[-1]]]],"d":{"foo": 12, "bar": "red"}}
        '''
    )

    validate_part1: int = 20
    validate_part2: int = 8

    # Set by post_init
    data = None

    def post_init(self) -> None:
        '''
        Load the JSON document into a data structure
        '''
        self.data: Any = json.loads(self.input)

    def part1(self) -> int:
        '''
        Return the sum of all numbers in the JSON document
        '''
        def _all_numbers(data: Any) -> Iterator[int]:
            if isinstance(data, int):
                yield data
            elif isinstance(data, dict):
                # JSON mapping keys are always strings so we only need to pay
                # attention to the values
                for value in data.values():
                    yield from _all_numbers(value)
            elif isinstance(data, (list, Iterator)):
                for value in data:
                    yield from _all_numbers(value)

        return sum(_all_numbers(self.data))

    def part2(self) -> int:
        '''
        Return the sum of all numbers in the JSON document, ignoring any nested
        JSON object containing a value of "red"
        '''
        def _ignore_red(data: Any) -> Iterator[int]:
            if isinstance(data, int):
                yield data
            elif isinstance(data, dict):
                # JSON mapping keys are always strings so we only need to pay
                # attention to the values
                if 'red' not in data.values():
                    for value in data.values():
                        yield from _ignore_red(value)
            elif isinstance(data, (list, Iterator)):
                for value in data:
                    yield from _ignore_red(value)

        return sum(_ignore_red(self.data))


if __name__ == '__main__':
    aoc = AOC2015Day12()
    aoc.run()
