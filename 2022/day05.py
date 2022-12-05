#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/5
'''
import re
from dataclasses import dataclass

# Local imports
from aoc2022 import AOC2022


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
    Implementation of a LIFO queue that is also iterable (i.e. contents can be
    inspected without being pulled off using .get()

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


class AOC2022Day5A(AOC2022):
    '''
    Base class for Day 3 of Advent of Code 2022
    '''
    day = 5

    def process_input(self) -> None:
        '''
        Load the initial stack state and process each move
        '''
        self.stacks = []
        self.moves = []

        # Read in the input
        with self.input.open() as fh:
            lines = fh.readlines()

        # Find the blank line dividing the stack definition and the moves list
        divider = lines.index('\n')

        # Create the stacks
        for _ in lines[divider - 1].rstrip('\n').split():
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

    def apply_moves(self) -> None:
        '''
        Apply the moves from the loaded stack
        '''
        for move in self.moves:
            items = self.stacks[move.old - 1].get(move.amount)
            if move.amount == 1:
                items = [items]
            self.stacks[move.new - 1].put(*items)

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


class AOC2022Day5B(AOC2022Day5A):
    '''
    Alternate implementation that takes into account the different method of
    crate arrangement from part two
    '''
    def apply_moves(self) -> None:
        '''
        Apply the moves from the loaded stack
        '''
        for move in self.moves:
            items = self.stacks[move.old - 1].get(move.amount)
            if move.amount == 1:
                items = [items]
            self.stacks[move.new - 1].put(*reversed(items))


if __name__ == '__main__':
    aoc1 = AOC2022Day5A()
    aoc1.apply_moves()
    answer1 = ''.join(aoc1.tops)
    print(f'Answer 1 (top item from each stack): {answer1}')
    aoc2 = AOC2022Day5B()
    aoc2.apply_moves()
    answer2 = ''.join(aoc2.tops)
    print(f"Answer 2 (top item from each stack): {answer2}")
