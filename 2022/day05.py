#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/5
'''
import re
import textwrap
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
        self.items: list[str] = []

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
    Day 5 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
        '''
    )

    validate_part1: str = 'CMZ'
    validate_part2: str = 'MCD'

    # Set by post_init
    stacks = None
    moves = None

    def post_init(self) -> None:
        '''
        Load the initial stack state and process each move
        '''
        self.stacks: list[Stack] = []
        self.moves: list[Move] = []

    def reset_stacks(self):
        '''
        Load the stacks and move list
        '''
        self.stacks.clear()
        self.moves.clear()

        lines: list[str] = self.input.splitlines(keepends=True)

        # Find the blank line dividing the stack definition and the moves list
        divider: int = lines.index('\n')

        # Create the stacks
        for _ in lines[divider - 1].rstrip().split():
            self.stacks.append(Stack())

        # Populate the stacks
        width: int = 4
        line: str
        for line in lines[divider - 2::-1]:
            index: int
            stack: Stack
            for index, stack in enumerate(self.stacks):
                start: int
                col: str
                start = index * width
                col = line[start:start + width].strip()
                if col:
                    stack.put(col.strip('[]'))

        move: re.Pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')

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
        ret: list[str] = []
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

        move: Move
        for move in self.moves:
            items: list[str] | str = self.stacks[move.old - 1].get(move.amount)
            if move.amount == 1:
                items: list[str] = [items]
            self.stacks[move.new - 1].put(*items)

        return ''.join(self.tops)

    def part2(self) -> str:
        '''
        The same as part 1, but move the crates in groups
        '''
        self.reset_stacks()

        move: Move
        for move in self.moves:
            items: list[str] | str = self.stacks[move.old - 1].get(move.amount)
            if move.amount == 1:
                items: list[str] = [items]
            self.stacks[move.new - 1].put(*reversed(items))

        return ''.join(self.tops)


if __name__ == '__main__':
    aoc = AOC2022Day5()
    aoc.run()
