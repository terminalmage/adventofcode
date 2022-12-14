#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/5

--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from
the ships. Supplies are stored in stacks of marked crates, but because the
needed supplies are buried under many other crates, the crates need to be
rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To
ensure none of the crates get crushed or fall over, the crane operator will
rearrange them in a series of carefully-planned steps. After the crates are
rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate
procedure, but they forgot to ask her which crate will end up where, and they
want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the
rearrangement procedure (your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two crates:
crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates;
from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a
single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a
quantity of crates is moved from one stack to a different stack. In the first
step of the above rearrangement procedure, one crate is moved from stack 2 to
stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

In the second step, three crates are moved from stack 1 to stack 3. Crates are
moved one at a time, so the first crate to be moved (D) ends up below the
second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates are
moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in
this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3,
so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each
stack?

--- Part Two ---

As you watch the crane operator expertly rearrange the crates, you notice the
process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly
wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air
conditioning, leather seats, an extra cup holder, and the ability to pick up
and move multiple crates at once.

Again considering the example above, the crates begin in the same
configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

However, the action of moving three crates from stack 1 to stack 3 means that
those three moved crates stay in the same order, resulting in this new
configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their order
as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now it's
crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally different
order: MCD.

Before the rearrangement process finishes, update your simulation so that the
Elves know where they should stand to be ready to unload the final supplies.
After the rearrangement procedure completes, what crate ends up on top of each
stack?
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
