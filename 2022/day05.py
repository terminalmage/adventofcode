#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/5
'''
import re
from dataclasses import dataclass

# Local imports
from aoc import AOC


@dataclass
class Move:
    '''
    Dataclass to represent a single move
    '''
    amount: int
    old: int
    new: int


class Stack:
    '''
    Implementation of a LIFO queue that is also iterable, i.e. contents can be
    inspected without being pulled off using .get().

    This is not a true queue implementation because all gets and puts are
    non-blocking, and there is no limit on queue size.
    '''
    def __init__(self) -> None:
        '''
        Create the list used to hold the stack items
        '''
        self.items = []

    def __repr__(self) -> str:
        '''
        Create the list used to hold the stack items
        '''
        return f'Stack([{", ".join(repr(item) for item in self.items)}])'

    def put(self, *items: tuple[str]) -> None:
        '''
        Add an item to the stack
        '''
        for item in items:
            self.items.insert(0, item)

    def get(self, amount: int=1) -> str | list[str]:
        '''
        Remove an item from the stack
        '''
        if amount > len(self):
            raise ValueError(
                f'Requested amount ({amount}) greated than stack size '
                f'({len(self)})'
            )

        ret = [self.items.pop(0) for _ in range(amount)]
        if amount == 1:
            return ret[0]

        return ret

    def __getitem__(self, index: int) -> str:
        '''
        Return the value of the requested stack index
        '''
        return self.items[index]

    def __len__(self) -> int:
        '''
        Return the size of the stack
        '''
        return len(self.items)


class AOC2022Day5(AOC):
    '''
    Day 5 of Advent of Code 2022 (first task)
    '''
    day = 5

    def __init__(self, example: bool = False) -> None:
        '''
        Load the initial stack state and process each move
        '''
        super().__init__(example=example)
        self.stacks = []
        self.moves = []

    def reset_stacks(self):
        '''
        Load the stacks and move list
        '''
        self.stacks.clear()
        self.moves.clear()

        # Read in the input
        with self.input.open() as fh:
            lines = fh.readlines()

        # Find the blank line dividing the stack definition and the moves list
        divider = lines.index('\n')

        # Create the stacks
        for _ in lines[divider - 1].rstrip().split():
            self.stacks.append(Stack())

        # Populate the stacks
        width = 4
        for line in lines[divider - 2::-1]:
            for index, stack in enumerate(self.stacks):
                start = index * width
                col = line[start:start + width].strip()
                if col:
                    stack.put(col.strip('[]'))

        move = re.compile(r'move (\d+) from (\d+) to (\d+)')

        # Parse the moves list
        for line in lines[divider + 1:]:
            self.moves.append(
                Move(*[int(item) for item in move.match(line).groups()])
            )

    @property
    def tops(self) -> list[str]:
        '''
        Return the top item from each stack. If a stack is empty, return a
        singls space character for that stack.
        '''
        ret = []
        for stack in self.stacks:
            try:
                ret.append(stack[0])
            except IndexError:
                ret.append(' ')
        return ret

    def part1(self) -> str:
        '''
        Apply the moves one crate at a time, returning the top of each stack
        '''
        self.reset_stacks()

        for move in self.moves:
            items = self.stacks[move.old - 1].get(move.amount)
            if move.amount == 1:
                items = [items]
            self.stacks[move.new - 1].put(*items)

        return ''.join(self.tops)

    def part2(self) -> str:
        '''
        The same as part 1, but move the crates in groups
        '''
        self.reset_stacks()

        for move in self.moves:
            items = self.stacks[move.old - 1].get(move.amount)
            if move.amount == 1:
                items = [items]
            self.stacks[move.new - 1].put(*reversed(items))

        return ''.join(self.tops)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day5(example=True)
    aoc.validate(aoc.part1(), 'CMZ')
    aoc.validate(aoc.part2(), 'MCD')
    # Run against actual data
    aoc = AOC2022Day5(example=False)
    aoc.run()
