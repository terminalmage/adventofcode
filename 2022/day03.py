#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/3
'''
from __future__ import annotations
import itertools
import string
from collections.abc import Generator, Iterator, Sequence

# Local imports
from aoc2022 import AOC2022


PRIORITY = {
    key: val for key, val in
    zip(string.ascii_lowercase, itertools.count(1))
}
PRIORITY.update({
    key: val for key, val in
    zip(string.ascii_uppercase, itertools.count(27))
})


class RucksackItem:
    '''
    Class to represent a single item from a RucksackCompartment
    '''
    def __init__(self, item: str):
        '''
        Create the item
        '''
        self.value = item

    def __repr__(self) -> str:
        '''
        Define repr() output for class
        '''
        return f'RucksackItem(value={self.value!r}, priority={self.priority})'

    def __eq__(self, rvalue: RucksackItem) -> bool:
        '''
        Implement '=' operator
        '''
        return self.priority == rvalue.priority

    def __lt__(self, rvalue: RucksackItem) -> bool:
        '''
        Implement '<' operator
        '''
        return self.priority < rvalue.priority

    def __gt__(self, rvalue: RucksackItem) -> bool:
        '''
        Implement '>' operator
        '''
        return self.priority > rvalue.priority

    def __le__(self, rvalue: RucksackItem) -> bool:
        '''
        Implement '<=' operator
        '''
        return self.priority <= rvalue.priority

    def __ge__(self, rvalue: RucksackItem) -> bool:
        '''
        Implement '>=' operator
        '''
        return self.priority >= rvalue.priority

    @property
    def value(self) -> str:
        '''
        Return the validated item value
        '''
        return self.__value

    @value.setter
    def value(self, item: str):
        '''
        Validate and set the item's value, and calculate the priority
        '''
        if item not in PRIORITY:
            raise ValueError(f'Invalid item {item!r}')

        self.__value = item
        self.priority = PRIORITY[item]


class RucksackCompartment:
    '''
    Represents a compartment within a Rucksack
    '''
    def __init__(self, items: Sequence[str]):
        '''
        Add the items to the compartment as individual RucksackItem instances
        '''
        self.items = [RucksackItem(item) for item in items]

    def __repr__(self) -> str:
        '''
        Define repr() output for class
        '''
        return f'RucksackCompartment([{", ".join(repr(item) for item in self.items)}])'

    def __iter__(self) -> Iterator[RucksackItem]:
        '''
        Iterate over items
        '''
        return iter(self.items)


class Rucksack:
    '''
    Class to represent a single Rucksack
    '''
    def __init__(self, items: Sequence[str]):
        '''
        Place the items into two separate compartments
        '''
        compartment_size = int(len(items) / 2)
        self.compartment1 = RucksackCompartment(items[:compartment_size])
        self.compartment2 = RucksackCompartment(items[compartment_size:])

    def __repr__(self) -> str:
        '''
        Define repr() output for class
        '''
        return (
            f'Rucksack(compartment1={self.compartment1!r}, '
            f'compartment2={self.compartment2!r})'
        )

    @property
    def items(self) -> Generator[RucksackItem, None, None]:
        '''
        Return a list of items that are in both compartments
        '''
        for item in self.compartment1:
            yield item
        for item in self.compartment2:
            yield item

    @property
    def duplicates(self) -> Generator[RucksackItem, None, None]:
        '''
        Return a list of items that are in both compartments
        '''
        return (
            RucksackItem(value)
            for value in set(
                c1item.value for c1item in self.compartment1
            ).intersection(
                set(
                    c2item.value for c2item in self.compartment2
                )
            )
        )


class AOC2022Day3(AOC2022):
    '''
    Base class for Day 3 of Advent of Code 2022
    '''
    day = 3

    def __init__(self):
        '''
        Initialize the data structure to hold the Rucksack objects
        '''
        super().__init__()

    def process_input(self):
        '''
        Load the rucksack contents
        '''
        self.rucksacks = []
        with self.input.open() as fh:
            for line in fh:
                self.rucksacks.append(Rucksack(line.rstrip('\n')))

    def groups(self, size=3) -> Generator[list[Rucksack], int, None]:
        '''
        Subdivide the rucksacks into groups of rucksacks
        '''
        start = 0
        while True:
            if not (group := self.rucksacks[start:start + size]):
                break
            yield group
            start += size

    def find_badge(self, group: list[Rucksack]) -> RucksackItem:
        '''
        Return a RucksackItem corresponding to the badge (the one item common
        to all Rucksacks in the group)
        '''
        if len(group) <= 1:
            raise ValueError('Group must have more than one member')

        itemset = {item.value for item in group[0].items}
        for othersack in group[1:]:
            itemset &= {item.value for item in othersack.items}

        if not itemset:
            raise ValueError('Group has no items in common')
        elif len(itemset) > 1:
            raise ValueError('Group has more than one item in common')

        return RucksackItem(list(itemset)[0])


if __name__ == '__main__':
    aoc = AOC2022Day3()
    answer1 = sum(
        sum(dup.priority for dup in rucksack.duplicates)
        for rucksack in aoc.rucksacks
    )
    print(f'Answer 1 (sum of priority of duplicate items):   {answer1}')
    answer2 = sum(aoc.find_badge(group).priority for group in aoc.groups())
    print(f"Answer 2 (sum of priority of each group's badge: {answer2}")
