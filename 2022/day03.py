#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/3

--- Day 3: Rucksack Reorganization ---

One Elf has the important job of loading all of the rucksacks with supplies for
the jungle journey. Unfortunately, that Elf didn't quite follow the packing
instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant
to go into exactly one of the two compartments. The Elf that did the packing
failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your
puzzle input), but they need your help finding the errors. Every item type is
identified by a single lowercase or uppercase letter (that is, a and A refer to
different types of items).

The list of items for each rucksack is given as characters all on a single
line. A given rucksack always has the same number of items in each of its two
compartments, so the first half of the characters represent items in the first
compartment, while the second half of the characters represent items in the
second compartment.

For example, suppose you have the following list of contents from six
rucksacks:

    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw

- The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means
  its first compartment contains the items vJrwpWtwJgWr, while the second
  compartment contains the items hcsFMMfFFhFp. The only item type that appears
  in both compartments is lowercase p.

- The second rucksack's compartments contain jqHRNqRjqzjGDLGL and
  rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is
  uppercase L.

- The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only
  common item type is uppercase P.

- The fourth rucksack's compartments only share item type v.

- The fifth rucksack's compartments only share item type t.

- The sixth rucksack's compartments only share item type s.

To help prioritize item rearrangement, every item type can be converted to a
priority:

- Lowercase item types a through z have priorities 1 through 26.

- Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both
compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19
(s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is
the sum of the priorities of those item types?

--- Part Two ---

As you finish identifying the misplaced items, the Elves come to you with
another issue.

For safety, the Elves are divided into groups of three. Every Elf carries a
badge that identifies their group. For efficiency, within each group of three
Elves, the badge is the only item type carried by all three Elves. That is, if
a group's badge is item type B, then all three Elves will have item type B
somewhere in their rucksack, and at most two of the Elves will be carrying any
other item type.

The problem is that someone forgot to put this year's updated authenticity
sticker on the badges. All of the badges need to be pulled out of the rucksacks
so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's
badges. The only way to tell which item type is the right one is by finding the
one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each
group can have a different badge item type. So, in the above example, the first
group's rucksacks are the first three lines:

    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg

And the second group's rucksacks are the next three lines:

    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw

In the first group, the only item type that appears in all three rucksacks is
lowercase r; this must be their badges. In the second group, their badge item
type must be Z.

Priorities for these items must still be found to organize the sticker
attachment efforts: here, they are 18 (r) for the first group and 52 (Z) for
the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. What
is the sum of the priorities of those item types?
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
