#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/17
'''
import collections
import hashlib
import textwrap
from collections.abc import Iterator
from typing import Literal

# Local imports
from aoc import AOC, Grid, XY

# Typing shortcuts
Passcode = str
VaultPath = str
Direction = Literal[b'U', b'D', b'L', b'R']
Move = tuple[XY, Direction]


class VaultGrid(Grid):
    '''
    Modified Grid class with puzzle-specific neighbor logic
    '''
    def __init__(self) -> None:
        '''
        Initialize the grid and find the start and end point
        '''
        # The vault area is a 4x4 grid of rooms. Simplify this to a 4x4
        # multi-line string, with S being your starting point and V being the
        # destination (i.e. the vault).
        super().__init__(
            textwrap.dedent(
                '''
                S***
                ****
                ****
                ***V
                '''
            ).strip()
        )
        self.start: XY = self.find('S')
        self.end: XY = self.find('V')
        self.move_sequence: tuple[Move, Move, Move, Move] = (
            (self.directions.NORTH, b'U'),
            (self.directions.SOUTH, b'D'),
            (self.directions.WEST, b'L'),
            (self.directions.EAST, b'R'),
        )

    def neighbors(  # pylint: disable=arguments-differ
        self,
        coord: XY,
        passcode: bytes,
    ) -> Iterator[Move]:
        '''
        Generator which yields a tuple of each neigbboring coordinate and the
        value stored at that coordinate.
        '''
        move: Move
        char: str
        for move, char in zip(
            self.move_sequence,
            hashlib.md5(passcode).hexdigest(),
        ):
            # The reason a greater-than comparison works here is because the ASCII
            # code for 9 is 57 and the codes for lowercase letters begin at 98.
            # This is quicker than a string/list/set/etc. membership check.
            if char > 'a':
                delta: XY
                direction: bytes
                delta, direction = move
                new_coord: XY = self.tuple_add(coord, delta)
                if new_coord in self:
                    yield new_coord, direction


class AOC2016Day17(AOC):
    '''
    Day 17 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        kglvqrro
        '''
    )

    validate_part1: str = 'DDUDRLRRUDRD'
    validate_part2: int = 492

    # Set by post_init
    grid = None
    passcode = None

    def post_init(self) -> None:
        '''
        Load the puzzle data
        '''
        self.grid: VaultGrid = VaultGrid()
        self.passcode: bytes = self.input.encode()

    def bfs(self) -> str:
        '''
        Find the shortest path to the vault
        '''
        dq: collections.deque[tuple[VaultPath, XY]] = collections.deque(
            [(b'', self.grid.start)]
        )

        path: VaultPath
        coord: XY
        neighbor: XY
        direction: Direction

        # This BFS will not use a "visited" set to track visited coordinates,
        # because a given coordinate can be visited more than once.
        while dq:
            path, coord = dq.popleft()

            if coord == self.grid.end:
                return path.decode()

            for neighbor, direction in self.grid.neighbors(
                coord,
                self.passcode + path,
            ):
                dq.append((path + direction, neighbor))

        raise RuntimeError(f'Passcode {self.passcode.decode()!r} is not valid')

    def dfs(self) -> set[VaultPath]:
        '''
        Find valid paths using DFS
        '''
        def _dfs(
            paths: set[VaultPath],
            start: XY = self.grid.start,
            path: bytes = b'',
        ) -> set[VaultPath]:
            '''
            Recursive depth-first function
            '''
            if start == self.grid.end:
                paths.add(path)
            else:
                for neighbor, direction in self.grid.neighbors(
                    start,
                    self.passcode + path
                ):
                    _dfs(paths, neighbor, path + direction)

            return paths

        paths: set[VaultPath] = set()
        return _dfs(paths)

    def part1(self) -> str:
        '''
        Find and return the shortest path to the destination, given the
        passcode and locking algorithm from the puzzle input.
        '''
        return self.bfs()

    def part2(self) -> int:
        '''
        Return the length of the longest path to the destination.
        '''
        return max(len(path) for path in self.dfs())


if __name__ == '__main__':
    aoc = AOC2016Day17()
    aoc.run()
