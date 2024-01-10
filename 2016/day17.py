#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/17
'''
import collections
import hashlib
import textwrap
from collections.abc import Generator
from typing import Literal

# Local imports
from aoc import AOC, Grid, XY

# Typing shortcuts
Passcode = str
VaultPath = str
Direction = Literal[b'U', b'D', b'L', b'R']


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

    def neighbors(  # pylint: disable=arguments-differ
        self,
        coord: XY,
        passcode: bytes,
    ) -> Generator[tuple[XY, Direction], None, None]:
        '''
        Generator which yields a tuple of each neigbboring coordinate and the
        value stored at that coordinate.
        '''
        in_grid = lambda r, c: 0 <= r <= self.max_row and 0 <= c <= self.max_col
        row, col = coord
        dir_abbrev: str = 'UDLR'
        # The reason a greater-than comparison works here is because the ASCII
        # code for 9 is 57 and the codes for lowercase letters begin at 98.
        # This is quicker than a string/list/set/etc. membership check.
        unlocked: frozenset[str] = frozenset({
            abbrev for abbrev, char in zip(
                dir_abbrev,
                hashlib.md5(passcode).hexdigest(),
            )
            if char > 'a'
        })
        # self.directions is in the order NSWE, or UDLR for the purposes of
        # this puzzle.
        for (row_delta, col_delta), direction in zip(self.directions, dir_abbrev):
            if direction in unlocked:
                new_row, new_col = row + row_delta, col + col_delta
                if in_grid(new_row, new_col):
                    yield (new_row, new_col), direction.encode()


class AOC2016Day17(AOC):
    '''
    Day 17 of Advent of Code 2016
    '''
    day: int = 17

    def __init__(self, example: bool = False) -> None:
        '''
        Load the puzzle data
        '''
        super().__init__(example=example)
        self.grid: VaultGrid = VaultGrid()
        self.passcode = b'kglvqrro' if self.example else b'vwbaicqe'

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
    # Run against test data
    aoc = AOC2016Day17(example=True)
    aoc.validate(aoc.part1(), 'DDUDRLRRUDRD')
    aoc.validate(aoc.part2(), 492)
    # Run against actual data
    aoc = AOC2016Day17(example=False)
    aoc.run()
