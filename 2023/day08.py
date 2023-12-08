#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/8
'''
import itertools
import math
from collections.abc import Callable

# Local imports
from aoc import AOC

# Typing shortcuts
NodeMap = dict[str, dict[str, str]]


class AOC2023Day8(AOC):
    '''
    Day 8 of Advent of Code 2023

    '''
    day = 8

    def load_input(self, part: int) -> tuple[str, NodeMap]:
        '''
        Load the input file
        '''
        data = self.get_input(part=part).read_text().splitlines()

        directions = data[0]
        node_map = {}

        for line in data[2:]:
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
        steps = 1
        node = start_node
        path = itertools.cycle(directions)

        while not condition(node := node_map[node][next(path)]):
            steps += 1

        return steps

    def part1(self) -> int:
        '''
        Return the number of steps to reach node ZZZ
        '''
        directions, node_map = self.load_input(part=1)

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
        directions, node_map = self.load_input(part=2)

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
    # Run against test data
    aoc = AOC2023Day8(example=True)
    aoc.validate(aoc.part1(), 6)
    aoc.validate(aoc.part2(), 6)
    # Run against actual data
    aoc = AOC2023Day8(example=False)
    aoc.run()
