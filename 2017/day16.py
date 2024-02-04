#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/16
'''
import re
import string
import textwrap
from collections.abc import Callable, Iterator
from typing import Literal

# Local imports
from aoc import AOC

# Type hints
Program = str
Programs = list[Program]
MoveParam = int | str
MoveFunc = Callable[[Programs, MoveParam, ...], None]
Move = tuple[MoveFunc, tuple[MoveParam, ...]]


class AOC2017Day16(AOC):
    '''
    Day 16 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        s1,x3/4,pe/b
        '''
    )

    validate_part1: str = 'baedc'

    # Set by post_init
    size = None
    moves = None

    def post_init(self) -> None:
        '''
        Set the program group size and load dance moves
        '''
        self.size: int = 5 if self.example else 16
        self.moves: tuple[Move, ...] = tuple(self.parse_moves(self.input))

    def parse_moves(self, moves: str) -> Iterator[Move]:
        '''
        Read in move definitions and yield Moves
        '''
        move_re: re.Pattern = re.compile(r'^([sxp])(.+)$')
        move_def: str
        for move_def in moves.split(','):
            move_type: Literal['s', 'x', 'p']
            params: str
            move_type, params = move_re.match(move_def).groups()
            match move_type:
                case 's':
                    yield self.spin, (int(params),)
                case 'x':
                    yield self.exchange, tuple(int(n) for n in params.split('/'))
                case 'p':
                    yield self.partner, tuple(params.split('/'))

    @staticmethod
    def spin(programs: Programs, count: int) -> None:
        '''
        Move the specified number of programs from the end to the front
        '''
        # Using [:] ensures the update happens in-place
        programs[:] = programs[-count:] + programs[:-count]

    @staticmethod
    def exchange(programs: Programs, a: int, b: int) -> None:
        '''
        Swap the programs at the specified indexes
        '''
        programs[a], programs[b] = programs[b], programs[a]

    def partner(self, programs: Programs, a: str, b: str) -> None:
        '''
        Swap the programs with the specified names
        '''
        idx_a: int = programs.index(a)
        idx_b: int = programs.index(b)
        self.exchange(programs, idx_a, idx_b)

    def lets_dance(self, programs: Programs) -> None:
        '''
        Put on your red shoes and dance the blues...
        '''
        move_func: MoveFunc
        move_params: tuple[MoveParam, ...]

        for move_func, move_params in self.moves:
            move_func(programs, *move_params)

    def part1(self) -> str:
        '''
        Return the positions of the programs after a single round
        '''
        programs: Programs = list(string.ascii_lowercase[:self.size])

        self.lets_dance(programs)
        return ''.join(programs)

    def part2(self) -> str:
        '''
        Return the positions of the programs after one billion rounds
        '''
        programs: Programs = list(self.part1())

        round_num: int = 0
        states: dict[str, int] = {}

        while True:
            self.lets_dance(programs)
            round_num += 1
            state: str = ''.join(programs)
            if state not in states:
                # Track the round number where this state was seen
                states[state] = round_num
            else:
                # Cycle length is the current round minus the round number the
                # last time this position was seen.
                cycle: int = round_num - states[state]
                # We need to simulate 1 billion rounds, _including_ the first
                # round we simulated. That leaves another 999,999,999 rounds.
                # Now that we know our cycle length, just divide that number of
                # remaining rounds by the cycle length and take the remainder.
                remaining: int = (999_999_999 - round_num) % cycle

                # Run the remaining number of rounds to get the final positions
                for _ in range(remaining):
                    self.lets_dance(programs)

                # Return the result
                return ''.join(programs)


if __name__ == '__main__':
    aoc = AOC2017Day16()
    aoc.run()
