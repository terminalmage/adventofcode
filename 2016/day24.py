#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/24
'''
import itertools
from collections import defaultdict, deque

# Local imports
from aoc import AOC, Grid, XY


class AOC2016Day24(AOC):
    '''
    Day 24 of Advent of Code 2016
    '''
    day = 24

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the computer and load the program from the puzzle input
        '''
        super().__init__(example=example)
        self.map: Grid = Grid(self.input)
        self.num_pos: dict[int, XY] = {}
        for row_num, row in enumerate(self.map.data):
            for col_num, col in enumerate(row):
                if col not in '#.':
                    try:
                        self.num_pos[int(col)] = (row_num, col_num)
                    except ValueError:
                        pass

        # Pre-calculate the distances between the map position of each digit
        self.distances: defaultdict[int, defaultdict[int, int]] = defaultdict(dict)
        start: int
        end: int
        for start, end in itertools.combinations(self.num_pos, 2):
            self.distances[start][end] = self.distances[end][start] = self.distance(
                start=self.num_pos[start],
                end=self.num_pos[end],
            )

    def distance(self, start: XY, end: XY) -> int:
        '''
        Use BFS to get the distance between two points
        '''
        # Type hints
        dist: int
        coord: XY
        neighbor: XY
        tile: str
        BFSKey = tuple[int, XY]

        visited: set[XY] = set()
        dq: deque[BFSKey] = deque([(0, start)])

        while dq:
            dist, coord = dq.popleft()

            if coord in visited:
                continue

            if coord == end:
                return dist

            visited.add(coord)

            dist += 1

            for (neighbor, tile) in self.map.neighbors(coord):
                if tile != '#':
                    dq.append((dist, neighbor))

        raise ValueError(f'Failed to find distance between {start} and {end}')

    def tsp(self, with_return: bool = False) -> int:
        '''
        Compute minimum distance using the graph generated from our
        pre-calculated distances.
        '''
        ret: int = 1e9
        stops: int = max(self.distances)
        route: tuple[int]
        for route in itertools.permutations(range(1, stops + 1)):
            # First get distance from start point (0) to first stop
            dist: int = self.distances[0][route[0]]
            # Now, add the distance between all the other stops
            stop: int
            for stop in range(1, len(route)):
                dist += self.distances[route[stop - 1]][route[stop]]
            if with_return:
                # Add the return trip from the last stop to the origin
                dist += self.distances[route[-1]][0]
            ret = min(ret, dist)
        return ret

    def part1(self) -> int:
        '''
        Find the shortest path to reach all the wires
        '''
        return self.tsp()

    def part2(self) -> int:
        '''
        Find the shortest path to reach all the wires and return home
        '''
        return self.tsp(with_return=True)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day24(example=True)
    aoc.validate(aoc.part1(), 14)
    # Run against actual data
    aoc = AOC2016Day24(example=False)
    aoc.run()
