#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/16
'''
import sys
import textwrap
from queue import SimpleQueue
from typing import Literal

# Local imports
from aoc import AOC, Grid, XY

# Type hints
StartState = dict[Literal['start', 'direction'], XY]

DEFAULT_START: XY = (0, 0)
DEFAULT_DIRECTION: XY = Grid.directions.EAST


class Contraption(Grid):
    '''
    Represents the Contraption from this puzzle
    '''
    reflections: dict[str, dict[XY, XY]] = {
        '\\': {
            Grid.directions.NORTH: Grid.directions.WEST,
            Grid.directions.SOUTH: Grid.directions.EAST,
            Grid.directions.WEST: Grid.directions.NORTH,
            Grid.directions.EAST: Grid.directions.SOUTH,
        },
        '/': {
            Grid.directions.NORTH: Grid.directions.EAST,
            Grid.directions.SOUTH: Grid.directions.WEST,
            Grid.directions.WEST: Grid.directions.SOUTH,
            Grid.directions.EAST: Grid.directions.NORTH,
        },
    }

    def shine_light(
        self,
        tasks: SimpleQueue,
        energized: set[XY],
        start: XY = DEFAULT_START,
        direction: XY = DEFAULT_DIRECTION,
    ) -> None:
        '''
        Simulate shining the light through the grid starting at the specified
        position and in the specified direction, returning a set of energized
        coordinates.
        '''
        # If the start point is outside the grid, the light is not in the grid
        if start not in self:
            return

        # Begin by energizing the starting coordinate
        energized.add(start)

        position: XY | None = None
        while (
            position := start if position is None
            else self.tuple_add(position, direction)
        ) in self:
            # Energize the current position
            energized.add(position)
            # Figure out what action (if any) to take
            match self[position]:
                case '-':
                    if direction in (
                        self.directions.NORTH,
                        self.directions.SOUTH,
                    ):
                        # Split the beam west and east
                        for new_direction in (
                            self.directions.WEST,
                            self.directions.EAST,
                        ):
                            tasks.put({
                                'start': position,
                                'direction': new_direction,
                            })
                        return
                case '|':
                    if direction in (
                        self.directions.WEST,
                        self.directions.EAST,
                    ):
                        # Split the beam north and south
                        for new_direction in (
                            self.directions.NORTH,
                            self.directions.SOUTH,
                        ):
                            tasks.put({
                                'start': position,
                                'direction': new_direction,
                            })
                        return
                case ('/' | '\\'):
                    # Bounce the beam using the reflections dict
                    direction = self.reflections[self[position]][direction]
                case '.':
                    # Do nothing
                    pass
                case _:
                    raise ValueError(
                        f'Unhandled grid character {self[position]!r}'
                    )

        return

    def run(
        self,
        start: XY = DEFAULT_START,
        direction: XY = DEFAULT_DIRECTION,
    ) -> int:
        '''
        Run a beam of light through the Contraption, returning the number of
        coordinates that are energized.
        '''
        # Initialize the task queue
        tasks: SimpleQueue[StartState] = SimpleQueue()
        tasks.put({'start': start, 'direction': direction})
        # Create sets to store the energized coordinates and the permutations
        # we've already called
        energized: set[XY] = set()
        calls: set[tuple[XY, XY]] = set()

        while not tasks.empty():
            kwargs: StartState = tasks.get(block=False)
            if (kwargs['start'], kwargs['direction']) in calls:
                continue
            # Run the task
            self.shine_light(
                tasks=tasks,
                energized=energized,
                **kwargs
            )
            # Add the task we just finished so we don't repeat it
            calls.add((kwargs['start'], kwargs['direction']))

        return len(energized)

    def best(self) -> int:
        '''
        Run all possible starting points and directions, returning the highest
        number of energized tiles this Contraption is capable of producing.
        '''
        calls: list[StartState] = []
        # Queue up all the coordinates in the top row
        calls.extend(
            {
                'start': (0, col),
                'direction': self.directions.SOUTH,
            }
            for col in range(self.cols)
        )
        # Queue up all the coordinates in the bottom row
        calls.extend(
            {
                'start': (self.rows - 1, col),
                'direction': self.directions.NORTH,
            }
            for col in range(self.cols)
        )
        # Queue up all the coordinates in the leftmost column
        calls.extend(
            {
                'start': (row, 0),
                'direction': self.directions.EAST,
            }
            for row in range(self.rows)
        )
        # Queue up all the coordinates in the rightmost column
        calls.extend(
            {
                'start': (row, self.cols - 1),
                'direction': self.directions.WEST,
            }
            for row in range(self.rows)
        )
        return max(self.run(**params) for params in calls)

    def print(self, energized: set[XY]) -> None:  # pylint: disable=arguments-differ
        '''
        Print the grid, with energized coordinates showing as "#" and
        non-energized coordinates showing as "."
        '''
        row_id: int
        for row_id in range(self.rows):
            sys.stdout.write(
                ''.join(
                    '#' if (row_id, col_id) in energized else '.'
                    for col_id in range(self.cols)
                ) + '\n'
            )
        sys.stdout.flush()

class AOC2023Day16(AOC):
    '''
    Day 16 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        r'''
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\
        ..../.\\..
        .-.-/..|..
        .|....-|.\
        ..//.|....
        '''
    )

    validate_part1: int = 46
    validate_part2: int = 51

    # Set by post_init
    contraption = None

    def post_init(self) -> None:
        '''
        Load the steps
        '''
        self.contraption: Contraption = Contraption(self.input)

    def part1(self) -> int:
        '''
        Return sum of hashes for each step
        '''
        return self.contraption.run()

    def part2(self) -> int:
        '''
        Calculate and return the lens' focusing power
        '''
        return self.contraption.best()


if __name__ == '__main__':
    aoc = AOC2023Day16()
    aoc.run()
