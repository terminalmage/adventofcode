#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/11
'''
from __future__ import annotations
import functools
import re
from collections.abc import Callable, Iterator, Sequence

# Third-party imports
import yaml

# Local imports
from aoc2022 import AOC2022

DEFAULT_CALM = True


def multiply_all(*items: Sequence[int]) -> int:
    '''
    Return the result of multiplying all the items in the sequence
    '''
    return functools.reduce(lambda x, y: x * y, *items)


class Barrel:
    '''
    A proper container for the monkeys
    '''
    def __init__(self, calm: bool = DEFAULT_CALM):
        '''
        Create an empty barrel
        '''
        self.__monkeys = {}
        self.calm = calm
        self.cm = None

    def __iter__(self) -> Iterator[Monkey]:
        '''
        Iterate over the monkeys in ID order
        '''
        for key in sorted(self.__monkeys):
            yield self[key]

    def __getitem__(self, num: int) -> Monkey:
        '''
        Get the monkey corresponding to the specified ID
        '''
        return self.__monkeys[num]

    def __setitem__(self, num: int, monkey: Monkey) -> None:
        '''
        Force .add() to be used
        '''
        raise NotImplementedError('use .add()')

    def add(self, monkey: Monkey) -> None:
        '''
        Add a monkey
        '''
        self.__monkeys[monkey.num] = monkey
        self.cm = multiply_all(item.divisible_by for item in self.__monkeys.values())

    def run(self, rounds: int) -> None:
        '''
        Run the specified number of rounds
        '''
        for _ in range(rounds):
            for monkey in self:
                #while (throw_to := monkey.inspect(calm=self.calm)) is not None:
                while monkey.items:
                    new_val = monkey.operation(monkey.items[0])
                    if self.calm:
                        # Reduce worry
                        new_val //= 3
                    else:
                        # "Find another way". The new value will be the modulus
                        # of the common multiplier.
                        new_val %= self.cm

                    monkey.items.pop(0)
                    monkey.inspected += 1

                    throw_to = monkey.on_true \
                        if new_val % monkey.divisible_by == 0 \
                        else monkey.on_false

                    self[throw_to].items.append(new_val)


class Monkey:
    '''
    Class to simulate monkey business
    '''
    def __init__(
        self,
        num: int,
        items: list[int],
        operation: Callable[[int], int],
        divisible_by: int,
        on_true: int,
        on_false: int,
    ) -> None:
        '''
        Initialize the monkey
        '''
        self.num = num
        self.items = items
        self.operation = operation
        self.divisible_by = divisible_by
        self.on_true = on_true
        self.on_false = on_false
        self.inspected = 0

    def __repr__(self) -> str:
        '''
        Define the repr() output
        '''
        return f'Monkey(num={self.num!r}, operation={self.operation!r}, divisible_by={self.divisible_by!r}, on_true={self.on_true!r}, on_false={self.on_false!r})'


class AOC2022Day11(AOC2022):
    '''
    Day 11 of Advent of Code 2022
    '''
    day = 11

    def load_monkeys(self) -> Iterator[Monkey]:
        '''
        Load the input and return a sequence of Monkey objects
        '''
        # Input is almost in yaml format, to "fix" it just realign the
        # If true/false lines using re.sub()
        data = yaml.safe_load(
            re.sub(
                r'^ +If (true|false):',
                r'  If \1:',
                self.input.read_text(),
                flags=re.MULTILINE,
            )
        )

        operation_re = re.compile(r'^new = old (\+|\*) (\d+|old)$')
        test_re = re.compile(r'^divisible by (\d+)$')
        throw_re = re.compile(r'^throw to monkey (\d+)$')

        for key, info in data.items():
            num = int(key.replace('Monkey ', ''))
            # Parse starting items
            items = [
                int(item.strip())
                for item in str(info['Starting items']).split(',')
            ]

            # Parse operation
            oper, mod = operation_re.match(info['Operation']).groups()
            operation = eval(f'lambda old: old {oper} {mod}')  # pylint: disable=eval-used

            # Parse test and success/fail conditions
            divisible_by = int(test_re.match(info['Test']).group(1))
            on_true = int(throw_re.match(info['If true']).group(1))
            on_false = int(throw_re.match(info['If false']).group(1))

            yield Monkey(
                num=num,
                items=items,
                operation=operation,
                divisible_by=divisible_by,
                on_true=on_true,
                on_false=on_false,
            )

    def commence_monkey_business(
        self,
        rounds: int,
        calm: bool = DEFAULT_CALM,
    ) -> int:
        '''
        Let's get down to (monkey) business!
        '''
        barrel = Barrel(calm=calm)
        for item in self.load_monkeys():
            barrel.add(item)
        barrel.run(rounds=rounds)

        return functools.reduce(
            lambda x, y: x * y,
            sorted((item.inspected for item in barrel), reverse=True)[:2]
        )

    def part1(self) -> int:
        '''
        Calculate the level of Monkey Business™ after 20 rounds, with
        worry-reduction logic enabled
        '''
        return self.commence_monkey_business(rounds=20)

    def part2(self) -> int:
        '''
        Calculate the level of Monkey Business™ after 10000 rounds, with
        worry-reduction logic disabled
        '''
        return self.commence_monkey_business(rounds=10000, calm=False)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day11(example=True)
    aoc.validate(aoc.part1(), 10605)
    aoc.validate(aoc.part2(), 2713310158)
    # Run against actual data
    aoc = AOC2022Day11(example=False)
    aoc.run()
