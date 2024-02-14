#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/9
'''
import re
import textwrap
from collections import defaultdict, deque

# Local imports
from aoc import AOC


class AOC2018Day9(AOC):
    '''
    Day 9 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        30 players; last marble is worth 5807 points
        '''
    )

    validate_part1: int = 37305

    # Set by post_init
    players = None
    high_marble = None

    def post_init(self) -> None:
        '''
        Load the numbers from the example data
        '''
        self.players: int
        self.high_marble: int
        self.players, self.high_marble = (
            int(n) for n in re.findall(r'\d+', self.input)
        )

    def solve(self, high: int) -> int:
        '''
        Simulate a game ending with a marble with the specified value
        '''
        scores: dict[int, int] = defaultdict(int)
        board: deque[int] = deque([0])

        marble: int
        for marble in range(1, high + 1):
            if marble % 23:
                board.rotate(-2)
                board.appendleft(marble)
            else:
                board.rotate(7)
                scores[marble % self.players] += (marble + board.popleft())

        return max(scores.values())

    def part1(self) -> int:
        '''
        Simulate using the value from the puzzle input
        '''
        return self.solve(high=self.high_marble)

    def part2(self) -> int:
        '''
        Simulate using the value from the puzzle input times 100
        '''
        return self.solve(high=self.high_marble * 100)


if __name__ == '__main__':
    aoc = AOC2018Day9()
    aoc.run()
