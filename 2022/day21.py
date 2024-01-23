#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/21
'''
import re
import sys

# Local imports
from aoc import AOC, oper_map

# Type hints
Expression = tuple[str, str, str]
Monkeys = dict[str, tuple[int | Expression]]


class AOC2022Day21(AOC):
    '''
    Day 21 of Advent of Code 2022
    '''
    def post_init(self) -> None:
        '''
        Load the monkeys into a data structure. If the monkey has an integer
        value associated with it, store that value. Otherwise, store a lambda
        that can be used to compute its value at a later time.
        '''
        monkey_re: re.Pattern = re.compile(
            r'([a-z]+): (?:(\d+)|([a-z]+) ([*/+-]) ([a-z]+))'
        )

        self.monkeys: Monkeys = {}
        for line in self.input.splitlines():
            name, value, lvalue, operand, rvalue = monkey_re.match(line).groups()
            if value is not None:
                self.monkeys[name] = int(value)
            else:
                self.monkeys[name] = (lvalue, operand, rvalue)

    def evaluate(
        self,
        name: str,
        monkeys: dict[str, float | Expression] | None = None,
        human: int | None = None,
    ) -> float:
        '''
        Calculate the value for the specified monkey
        '''
        if monkeys is None:
            monkeys = self.monkeys.copy()
        if human is not None:
            monkeys['humn'] = human

        value = monkeys[name]
        try:
            # Retrieve the lvalue and rvalue for the arithmetic expression,
            # computing those values if needed
            lvalue: float = self.evaluate(value[0], monkeys=monkeys)
            rvalue: float = self.evaluate(value[2], monkeys=monkeys)
            # Evaluate the value for the monkey
            monkeys[name] = oper_map[value[1]](lvalue, rvalue)
            # Return the evaluated result
            return monkeys[name]
        except TypeError:
            # The monkey already has an integer value assigned to it
            return value

    @staticmethod
    def normalize(value: int) -> int:
        '''
        If the value is an int, return an integer type
        '''
        int_value: int = int(value)
        if value == int_value:
            return int_value
        return value

    def part1(self) -> int | float:
        '''
        Decrypt the cipher and return the coordinates
        '''
        return self.normalize(self.evaluate('root'))

    def part2(self) -> int | float:
        '''
        Figure out the correct value to use for the "humn" variable, to make
        the two components of the root monkey's equation equal, using a binary
        search.
        '''
        left: str
        right: str
        left, right = self.monkeys['root'][0], self.monkeys['root'][2]

        def _get_diff(human: int) -> int:
            '''
            Calculate both left and right monkeys with the specified value for
            the "humn" variable, and return the difference
            '''
            monkeys: Monkeys = self.monkeys.copy()
            lvalue: int = self.evaluate(left, monkeys=monkeys, human=human)
            rvalue: int = self.evaluate(right, monkeys=monkeys, human=human)
            return lvalue - rvalue

        modifier: True = _get_diff(1) > 0

        low: int = 0
        high: int = sys.maxsize

        while True:
            # Select the midpoint between low and high
            human: int = (low + high) // 2

            # Evaluate both lvalue and rvalue using this value for "humn"
            diff: int = _get_diff(human)

            if not diff:
                # Both lvalue and rvalue were identical, break out of loop
                break

            if human == low:
                # No match found
                raise RuntimeError('Binary search failed')

            if diff > 0:
                if modifier:
                    low = human
                else:
                    high = human
            else:
                if modifier:
                    high = human
                else:
                    low = human

        return self.normalize(human)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day21(example=True)
    aoc.validate(aoc.part1(), 152)
    aoc.validate(aoc.part2(), 301)
    # Run against actual data
    aoc = AOC2022Day21(example=False)
    aoc.run()
