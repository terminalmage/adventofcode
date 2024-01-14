#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/22
'''
import collections
import itertools
import re
import sys
from collections.abc import Generator
from dataclasses import dataclass

# Local imports
from aoc import AOC, XY, directions


@dataclass(frozen=True)
class StorageNode:
    '''
    Collects stats for a given storage node
    '''
    x: int
    y: int
    size: int
    used: int
    avail: int
    percent: int


class StorageGrid(dict):
    '''
    Dict subclass to manage a system of StorageNode objects
    '''
    def add_node(
        self,
        x: int,
        y: int,
        size: int,
        used: int,
        avail: int,
        percent: int,
    ) -> None:
        '''
        Add a new StorageNode
        '''
        self[(x, y)] = StorageNode(
            x=x,
            y=y,
            size=size,
            used=used,
            avail=avail,
            percent=percent,
        )

    def neighbors(self, x: int, y: int) -> Generator[StorageNode, None, None]:
        '''
        Return the neighboring StorageNode instances
        '''
        x_delta: int
        y_delta: int
        for x_delta, y_delta in directions:
            try:
                yield self[(x + x_delta, y + y_delta)]
            except KeyError:
                continue


class AOC2016Day22(AOC):
    '''
    Day 22 of Advent of Code 2016
    '''
    day: int = 22

    def __init__(self, example: bool = False) -> None:
        '''
        Load puzzle input as a sorted sequence of IP ranges
        '''
        super().__init__(example=example)
        self.grid: StorageGrid = StorageGrid()
        with self.input.open() as fh:
            for line in fh:
                try:
                    x, y, size, used, avail, percent = (
                        int(m) for m in re.findall(r'\d+', line)
                    )
                except ValueError:
                    continue
                self.grid.add_node(x, y, size, used, avail, percent)
                if used == 0:
                    self.empty = self.grid[(x, y)]

        self.max_x: int
        self.max_y: int
        self.max_x, self.max_y = map(max, zip(*self.grid))

    def print_grid(self) -> None:
        '''
        Print the grid to stdout. The nodes are represented by the following
        characters:

            - Empty node: _
            - "Wall" nodes: #
            - Goal data: G
            - Destination node: D
            - All other nodes: .
        '''
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                node_id: XY = (x, y)
                if node_id == (0, 0):
                    sys.stdout.write('D')
                elif node_id == (self.max_x, 0):
                    sys.stdout.write('G')
                else:
                    node = self.grid[node_id]
                    if node.percent > 85:
                        sys.stdout.write('#')
                    elif node.percent == 0:
                        sys.stdout.write('_')
                    else:
                        sys.stdout.write('.')
            sys.stdout.write('\n')

    def part1(self) -> int:
        '''
        Return number of viable node pairs
        '''
        return sum(
            node1.used and node1.used <= node2.avail
            for node1, node2 in itertools.permutations(self.grid.values(), 2)
        )

    def part2(self) -> int:
        '''
        Find and return the fewest number of steps to get the data from the
        goal node to the dest node
        '''
        # Type hints
        dist: int
        node: StorageNode
        BFSKey = tuple[int, StorageNode]

        visited: set[StorageNode] = set()
        dq: collections.deque[BFSKey] = collections.deque([(0, self.empty)])
        goal: StorageNode = self.grid[(self.max_x - 1, 0)]
        empty_to_goal: int = 0

        # The first step is a BFS to find the distance the empty node needs to
        # travel to reach the goal, which is to the left of the node with the
        # goal data. There is no need to treat the "wall" nodes specially, a
        # valid move is simply one in which the "used" amount of the
        # neighboring node is <= the size of the current node (so the data from
        # that node can fit into the current node.
        while dq:
            dist, node = dq.popleft()

            if node in visited:
                continue

            if node is goal:
                empty_to_goal = dist
                break

            visited.add(node)

            dist += 1

            for neighbor in self.grid.neighbors(node.x, node.y):
                if neighbor.used <= node.size:
                    dq.append((dist, neighbor))

        # Make that a path to the goal was successfully found
        assert empty_to_goal

        # From the goal (one left of the goal data), we need to perform a
        # repeating pattern of moves which will eventually get the empty node
        # into the desired position at (0, 0). The empty node first needs to
        # move to the right (to swap the goal data into its position). The
        # empty node then needs to move down, left, left, and up, after which
        # the process repeats. Performing this sequence of 5 moves a number of
        # times equal to the x value of the goal, will put the empty node at
        # (0, 0). From here you just need one final shift of the data to put
        # the goal data into that node.
        return empty_to_goal + (goal.x * 5) + 1


if __name__ == '__main__':
    aoc = AOC2016Day22(example=True)
    aoc.validate(aoc.part1(), 7)
    aoc.validate(aoc.part2(), 7)
    # Run against actual data
    aoc = AOC2016Day22(example=False)
    aoc.run()
