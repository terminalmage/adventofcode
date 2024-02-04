#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/8
'''
from __future__ import annotations
import textwrap

# Local imports
from aoc import AOC

# Type hints
Numbers = tuple[int, ...]


class Node:
    '''
    Node which can contain zero or more child nodes
    '''
    def __init__(self, numbers: Numbers) -> None:
        '''
        Load the node and any child nodes
        '''
        num_children: int
        num_metadata: int
        num_children, num_metadata = numbers[:2]

        self.children: list[Node] = []
        index: int = 2

        for _ in range(num_children):
            self.children.append(Node(numbers[index:]))
            index += self.children[-1].length

        self.metadata: tuple[int, ...] = tuple(numbers[index:index + num_metadata])
        self.length: int = index + num_metadata

    @property
    def metadata_recursive(self) -> int:
        '''
        Return the sum of this Node's metadata and that of all of its child
        nodes, recursively.
        '''
        return sum(self.metadata) + sum(
            node.metadata_recursive for node in self.children
        )

    @property
    def value(self) -> int:
        '''
        Return the value of this node, as defined in Part 2 of the puzzle
        '''
        if self.children:
            total: int = 0
            # Return the sum of the specified children's metadata
            index: int
            for index in (n - 1 for n in self.metadata):
                try:
                    total += self.children[index].value
                except IndexError:
                    continue
            return total

        # No children, so return the sum of the metadata entries
        return sum(self.metadata)


class AOC2018Day8(AOC):
    '''
    Day 8 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
        '''
    )

    validate_part1: int = 138
    validate_part2: int = 66

    # Set by post_init
    tree = None

    def post_init(self) -> None:
        '''
        Load the numbers from the example data
        '''
        self.tree: Node = Node(tuple(int(n) for n in self.input.split()))

    def part1(self) -> int:
        '''
        Return the sum of all metadata entries
        '''
        return self.tree.metadata_recursive

    def part2(self) -> int:
        '''
        Return the value of the root node
        '''
        return self.tree.value


if __name__ == '__main__':
    aoc = AOC2018Day8()
    aoc.run()
