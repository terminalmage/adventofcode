#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/22
'''
import math
import textwrap
from collections import Counter, defaultdict, deque
from enum import Enum

# Local imports
from aoc import AOC, TupleMixin, XY, directions

# Type hints
VirusGrid = defaultdict[XY, str]


class Status(Enum):
    '''
    Aggregates status values for use in match statements during simulation
    '''
    INFECTED: str = '#'
    CLEAN: str = '.'
    WEAKENED: str = 'W'
    FLAGGED: str = 'F'


class Virus(TupleMixin):
    '''
    Simulates the progression of the virus
    '''
    def __init__(self, initial_state: str) -> None:
        '''
        Load the input. Note that some of this resembles the Grid class from
        the aoc lib, but since we need to expand outwards, we can't use that
        class here.
        '''
        # Assigned whenever .reset() is run
        self.grid = self.position = self.directions = self.infections = None
        self.initial_state: str = initial_state
        self.reset()

    def reset(self) -> VirusGrid:
        '''
        Load the initial state into a new VirusGrid and reset the starting
        position back to the middle of that grid.
        '''
        grid: defaultdict[XY, str] = defaultdict(lambda: Status.CLEAN.value)

        row_index: int
        col_index: int
        row: str
        col: str
        for row_index, row in enumerate(self.initial_state.splitlines()):
            for col_index, col in enumerate(row):
                grid[(row_index, col_index)] = col

        self.grid = grid

        # Start in the middle
        self.position: XY = math.ceil(row_index / 2), math.ceil(col_index / 2)

        # The directions namedtuple begins with NORTH (i.e. "up"), so no
        # further manipulation needs to be done.
        self.directions: deque[XY] = deque(directions)

        # Reset infection count to 0
        self.infections: int = 0

    @property
    def facing(self) -> XY:
        '''
        Return XY delta of current direction
        '''
        return self.directions[0]

    @property
    def infected(self) -> int:
        '''
        Return the number of infected
        '''
        try:
            return Counter(self.grid.values())[Status.INFECTED.value]
        except KeyError:
            return 0

    def simulate(self, part: int, rounds: int):
        '''
        Simulate the movement and effects of the virus. See the following for
        descriptions of the virus behavior:

        - Part 1: https://adventofcode.com/2017/day/22
        - Part 2: https://adventofcode.com/2017/day/22#part2
        '''
        self.reset()

        # Directional constants. These are used to rotate the deque containing
        # directional movement deltas.
        LEFT: int = 1
        RIGHT: int = -1
        REVERSE: int = 2

        match part:

            case 1:
                for _ in range(rounds):
                    match self.grid[self.position]:
                        case Status.INFECTED.value:
                            self.directions.rotate(RIGHT)
                            self.grid[self.position] = Status.CLEAN.value
                        case Status.CLEAN.value:
                            self.directions.rotate(LEFT)
                            self.grid[self.position] = Status.INFECTED.value
                            self.infections += 1
                        case _:
                            raise ValueError(
                                f'Invalid status marker '
                                f'{self.grid[self.position]!r} found at '
                                f'position {self.position}'
                            )
                    self.position = self.tuple_add(self.position, self.facing)

            case 2:
                for _ in range(rounds):
                    match self.grid[self.position]:
                        case Status.CLEAN.value:
                            self.directions.rotate(LEFT)
                            self.grid[self.position] = Status.WEAKENED.value
                        case Status.WEAKENED.value:
                            self.grid[self.position] = Status.INFECTED.value
                            self.infections += 1
                        case Status.INFECTED.value:
                            self.directions.rotate(RIGHT)
                            self.grid[self.position] = Status.FLAGGED.value
                        case Status.FLAGGED.value:
                            self.directions.rotate(REVERSE)
                            self.grid[self.position] = Status.CLEAN.value
                        case _:
                            raise ValueError(
                                f'Invalid status marker '
                                f'{self.grid[self.position]!r} found at '
                                f'position {self.position}'
                            )
                    self.position = self.tuple_add(self.position, self.facing)

            case _:
                raise ValueError(f'Invalid part: {part!r}')


class AOC2017Day22(AOC):
    '''
    Day 22 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        ..#
        #..
        ...
        '''
    )

    validate_part1: int = 5587
    validate_part2: int = 26

    def part1(self) -> int:
        '''
        Simulate using the criteria from Part 1
        '''
        virus: Virus = Virus(self.input)
        virus.simulate(part=1, rounds=10_000)
        return virus.infections

    def part2(self) -> int:
        '''
        Simulate using the criteria from Part 2
        '''
        virus: Virus = Virus(self.input)
        virus.simulate(part=2, rounds=100 if self.example else 10_000_000)
        return virus.infections


if __name__ == '__main__':
    aoc = AOC2017Day22()
    aoc.run()
