#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/12
'''
import json
from collections.abc import Iterator
from typing import Any

# Local imports
from aoc import AOC


class AOC2015Day12(AOC):
    '''
    Day 12 of Advent of Code 2015
    '''
    day = 12

    def __init__(self, example: bool = False) -> None:
        '''
        Load the JSON document into a data structure
        '''
        super().__init__(example=example)
        self.data = json.loads(self.input.read_text().strip())

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
                    for item in _all_numbers(value):
                        yield item
            elif isinstance(data, (list, Iterator)):
                for value in data:
                    for item in _all_numbers(value):
                        yield item

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
                        for item in _ignore_red(value):
                            yield item
            elif isinstance(data, (list, Iterator)):
                for value in data:
                    for item in _ignore_red(value):
                        yield item

        return sum(_ignore_red(self.data))


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day12(example=True)
    aoc.validate(aoc.part1(), 20)
    aoc.validate(aoc.part2(), 8)
    # Run against actual data
    aoc = AOC2015Day12(example=False)
    aoc.run()
