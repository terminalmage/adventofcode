#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/12

--- Day 12: JSAbacusFramework.io ---

Santa's Accounting-Elves need help balancing the books after a recent order.
Unfortunately, their accounting software uses a peculiar storage format. That's
where you come in.

They have a JSON document which contains a variety of things: arrays ([1,2,3]),
objects ({"a":1, "b":2}), numbers, and strings. Your first job is to simply
find all of the numbers throughout the document and add them together.

For example:

- [1,2,3] and {"a":2,"b":4} both have a sum of 6.

- [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.

- {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.

- [] and {} both have a sum of 0.

You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?

--- Part Two ---

Uh oh - the Accounting-Elves have realized that they double-counted everything
red.

Ignore any object (and all of its children) which has any property with the
value "red". Do this only for objects ({...}), not arrays ([...]).

- [1,2,3] still has a sum of 6.

- [1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is
  ignored.

- {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0, because the entire
  structure is ignored.

- [1,"red",5] has a sum of 6, because "red" in an array has no effect.
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
