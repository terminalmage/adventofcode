#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/23
'''
import textwrap
from collections import deque
from collections.abc import Iterator

# Local imports
from aoc import AOC, Grid, XY

# Typing shortcuts
Branch = tuple[XY, int]
Graph = dict[XY, list[Branch]]


class DeadEnd(Exception):
    '''
    Custom class to facilitate breaking out of multiple looping levels at the
    same time.
    '''


class HikingPath(Grid):
    '''
    Modified Grid object with puzzle-specific movement rules
    '''
    def __init__(self, data: str) -> None:  # pylint: disable=arguments-differ
        '''
        Add path entrance/exit
        '''
        super().__init__(data)
        self.entrance: XY = (0, 1)
        self.exit: XY = (self.max_row, self.max_col - 1)

    def neighbors(  # pylint: disable=arguments-differ
        self,
        coord: XY,
        slopes_traversable: bool = False
    ) -> Iterator[XY]:
        '''
        Generator which yields a tuple of each neigbboring coordinate and the
        value stored at that coordinate.
        '''
        tile: str
        try:
            tile = self[coord]
        except (TypeError, IndexError):
            # This is position is outside the grid, set it to a forest tile to
            # trigger a ValueError below.
            tile = '#'

        if slopes_traversable and tile != '#':
            # Ensure that slopes are treated like normal tiles, for the purpose
            # of selecting possible directions in the match statement below.
            tile = '.'

        possible: tuple[XY, ...]
        match tile:
            case '.':
                possible = self.directions
            case '>':
                possible = (self.directions.EAST,)
            case 'v':
                possible = (self.directions.SOUTH,)
            case '<':
                possible = (self.directions.WEST,)
            case '^':
                possible = (self.directions.NORTH,)
            case _:
                raise ValueError(f'Invalid position: {coord}')

        for direction in possible:
            new_row: int
            new_col: int
            new_row, new_col = self.tuple_add(coord, direction)
            try:
                if (
                    new_row >= 0 and new_col >= 0
                    and self.data[new_row][new_col] != '#'
                ):
                    yield new_row, new_col
            except IndexError:
                pass

    def build_graph(self, slopes_traversable: bool = False) -> Graph:
        '''
        Use the contents of the grid to construct a Graph.

        All branching intersections will be nodes on the graph. In addition,
        if slopes are not traversable (i.e. you must follow a slope and cannot
        traverse it in the opposite direction it points), then coordinates
        containing slopes will also be added to the graph.
        '''
        nodes: deque[XY] = deque([(0, 1)])
        visited: set[XY] = set()
        graph: Graph = {}
        while nodes:
            node = nodes.pop()

            if node in visited:
                continue

            visited.add(node)
            graph[node] = []

            cur: XY
            for cur in self.neighbors(node, slopes_traversable):
                prev: XY = node
                distance: int = 1
                try:
                    while True:
                        neighbors: list[XY] = list(
                            self.neighbors(cur, slopes_traversable)
                        )
                        if neighbors == [prev] and self[cur] in '>v<^':
                            # Traversal has hit a slope head-on and cannot move
                            # in any direction but reverse (not allowed)
                            raise DeadEnd
                        if len(neighbors) != 2:
                            # If the number of neighbors is 1, then we've hit a
                            # slope, and the reverse direction is not included
                            # in the return from the self.neighbors generator.
                            # Note that travel in reverse is not allowed, but
                            # the absence of the reverse direction in the list
                            # of neighbors is what we use to detect slopes.
                            #
                            # If the number of neighbors is greater than 2,
                            # then we've reached an intersection. In either
                            # case, the current point is a new node.  Break out
                            # of the loop to add the new node.
                            break

                        neighbor: XY
                        for neighbor in neighbors:
                            if neighbor == prev:
                                continue
                            # Increment distance
                            distance += 1
                            # Update pointers and continue walking the path
                            cur, prev = neighbor, cur
                            break
                except DeadEnd:
                    continue
                # Add a new node at the current position
                nodes.append(cur)
                # Note the difference between the current node and the node
                # we've just discovered.
                graph[node].append((cur, distance))

        return graph

    def longest_hike(
        self,
        slopes_traversable: bool = False,
    ) -> int:
        '''
        Derive the longest possible hike given the path defined in the puzzle
        input. If slopes_traversable is True, then traversal will continue
        "uphill" if a slope is reached, while the default behavior is to treat
        that as a dead end.
        '''
        graph: Graph = self.build_graph(slopes_traversable=slopes_traversable)
        # This deque will track the following for each simulated hike:
        #   1. Visited nodes
        #   2. The latest node visited
        #   3. The cumulative length hiked
        lifo: deque[tuple[frozenset[XY], XY, int]]
        # Start at the entrance (of course)
        lifo = deque([
            (frozenset({self.entrance}), self.entrance, 0)
        ])
        # Aggregates completed hikes
        lengths: set[int] = set()

        while lifo:
            visited, node, length = lifo.pop()
            if node == self.exit:
                # If the current node is the exit node, the hike is completed.
                # Make note of the length and continue processing the queue.
                lengths.add(length)
                continue
            # From the current node, try all connected nodes defined in the
            # graph.
            for next_node, leg_length in graph[node]:
                if next_node not in visited:
                    lifo.append(
                        (visited | {next_node}, next_node, length + leg_length)
                    )

        return max(lengths)


class AOC2023Day23(AOC):
    '''
    Day 23 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        #.#####################
        #.......#########...###
        #######.#########.#.###
        ###.....#.>.>.###.#.###
        ###v#####.#v#.###.#.###
        ###.>...#.#.#.....#...#
        ###v###.#.#.#########.#
        ###...#.#.#.......#...#
        #####.#.#.#######.#.###
        #.....#.#.#.......#...#
        #.#####.#.#.#########v#
        #.#...#...#...###...>.#
        #.#.#v#######v###.###v#
        #...#.>.#...>.>.#.###.#
        #####v#.#.###v#.#.###.#
        #.....#...#...#.#.#...#
        #.#########.###.#.#.###
        #...###...#...#...#.###
        ###.###.#.###v#####v###
        #...#...#.#.>.>.#.>.###
        #.###.###.#.###.#.#v###
        #.....###...###...#...#
        #####################.#
        '''
    )

    validate_part1: int = 94
    validate_part2: int = 154

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.path: HikingPath = HikingPath(self.input)

    def part1(self) -> int:
        '''
        Calculate the longest possible hike if slopes are not traversable.
        '''
        return self.path.longest_hike()

    def part2(self) -> int:
        '''
        Calculate the longest possible hike if slopes *are* traversable.
        '''
        return self.path.longest_hike(slopes_traversable=True)


if __name__ == '__main__':
    aoc = AOC2023Day23()
    aoc.run()
