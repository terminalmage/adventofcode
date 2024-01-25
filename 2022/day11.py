#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/11
'''
from __future__ import annotations
import math
import re
import textwrap
from collections.abc import Callable, Iterator

# Local imports
from aoc import AOC

DEFAULT_CALM = True


class Barrel:
    '''
    A proper container for the monkeys
    '''
    def __init__(self, calm: bool = DEFAULT_CALM):
        '''
        Create an empty barrel
        '''
        self.__monkeys: dict[int, Monkey] = {}
        self.calm = calm
        self.cm = None

    def __iter__(self) -> Iterator[Monkey]:
        '''
        Iterate over the monkeys in ID order
        '''
        key: int
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
        self.cm: int = math.prod(item.divisible_by for item in self.__monkeys.values())

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
        self.num: int = num
        self.items: list[int] = items
        self.operation: Callable[[int], int] = operation
        self.divisible_by: int = divisible_by
        self.on_true: int = on_true
        self.on_false: int = on_false
        self.inspected: int = 0

    def __repr__(self) -> str:
        '''
        Define the repr() output
        '''
        return f'Monkey(num={self.num!r}, operation={self.operation!r}, divisible_by={self.divisible_by!r}, on_true={self.on_true!r}, on_false={self.on_false!r})'


class AOC2022Day11(AOC):
    '''
    Day 11 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        Monkey 0:
          Starting items: 79, 98
          Operation: new = old * 19
          Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3

        Monkey 1:
          Starting items: 54, 65, 75, 74
          Operation: new = old + 6
          Test: divisible by 19
            If true: throw to monkey 2
            If false: throw to monkey 0

        Monkey 2:
          Starting items: 79, 60, 97
          Operation: new = old * old
          Test: divisible by 13
            If true: throw to monkey 1
            If false: throw to monkey 3

        Monkey 3:
          Starting items: 74
          Operation: new = old + 3
          Test: divisible by 17
            If true: throw to monkey 0
            If false: throw to monkey 1
        '''
    )

    validate_part1: int = 10605
    validate_part2: int = 2713310158

    def load_monkeys(self) -> Iterator[Monkey]:
        '''
        Load the input and return a sequence of Monkey objects
        '''
        for (
            num, starting_items, oper, mod, divisible_by, on_true, on_false
        ) in re.findall(
            r'Monkey (\d+):\n'
            r'\s*Starting items: ([0-9, ]+)\n'
            r'\s*Operation: new = old (\+|\*) (\d+|old)\n'
            r'\s*Test: divisible by (\d+)\n'
            r'\s*If true: throw to monkey (\d+)\n'
            r'\s*If false: throw to monkey (\d+)',
            self.input,
            flags=re.MULTILINE,
        ):
            yield Monkey(
                num=int(num),
                items=[int(item.strip()) for item in starting_items.split(',')],
                operation=eval(f'lambda old: old {oper} {mod}', {}, {}),  # pylint: disable=eval-used
                divisible_by=int(divisible_by),
                on_true=int(on_true),
                on_false=int(on_false),
            )

    def commence_monkey_business(
        self,
        rounds: int,
        calm: bool = DEFAULT_CALM,
    ) -> int:
        '''
        Let's get down to (monkey) business!
        '''
        barrel: Barrel = Barrel(calm=calm)
        item: Monkey
        for item in self.load_monkeys():
            barrel.add(item)
        barrel.run(rounds=rounds)

        return math.prod(
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
    aoc = AOC2022Day11()
    aoc.run()
