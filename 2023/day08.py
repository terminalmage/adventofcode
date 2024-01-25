#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/8
'''
import itertools
import math
import textwrap
from collections.abc import Callable, Sequence
from typing import Literal

# Local imports
from aoc import AOC

# Typing shortcuts
Direction = Literal['L', 'R']
NodeMap = dict[str, dict[Direction, str]]


class AOC2023Day8(AOC):
    '''
    Day 8 of Advent of Code 2023

    '''
    example_data_part1: str = textwrap.dedent(
        '''
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        '''
    )
    example_data_part2: str = textwrap.dedent(
        '''
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        '''
    )

    validate_part1: int = 6
    validate_part2: int = 6

    def load(self, data: str) -> tuple[str, NodeMap]:
        '''
        Load the input file
        '''
        lines: list[str] = data.splitlines()

        directions: str = lines[0]
        node_map: NodeMap = {}

        for line in lines[2:]:
            name: str
            left: str
            right: str
            name, _, left, right = line.split()
            left = left.strip('(,')
            right = right.strip(')')
            node_map[name] = {'L': left, 'R': right}

        return directions, node_map

    def traverse(
        self,
        node_map: NodeMap,
        start_node: str,
        directions: str,
        condition: Callable[[str], bool],
    ) -> int:
        '''
        Traverse the node map, returning the number of steps before the
        condition returns True.
        '''
        steps: int = 1
        node: str = start_node
        path: Sequence[Direction] = itertools.cycle(directions)

        while not condition(node := node_map[node][next(path)]):
            steps += 1

        return steps

    def part1(self) -> int:
        '''
        Return the number of steps to reach node ZZZ
        '''
        directions: str
        node_map: NodeMap
        directions, node_map = self.load(self.input_part1)

        return self.traverse(
            node_map=node_map,
            start_node='AAA',
            directions=directions,
            condition=lambda node: node == 'ZZZ',
        )

    def part2(self) -> int:
        '''
        Return the number of steps it takes before concurrent traversals
        starting at all start nodes (those ending in "A") simultaneously arrive
        at an exit node (one ending in "Z").

        This is calculated by deriving the lowest common multiple of the steps
        it takes to traverse from each start node to any exit node.
        '''
        directions: str
        node_map: NodeMap
        directions, node_map = self.load(self.input_part2)

        return math.lcm(
            *(
                self.traverse(
                    node_map=node_map,
                    start_node=start_node,
                    directions=directions,
                    condition=lambda node: node.endswith('Z'),
                )
                for start_node in (
                    node for node in node_map
                    if node.endswith('A')
                )
            )
        )


if __name__ == '__main__':
    aoc = AOC2023Day8()
    aoc.run()
