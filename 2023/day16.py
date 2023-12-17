#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/16
'''
import queue
import sys
from pathlib import Path

# Local imports
from aoc import AOC

# Typing shortcuts
Coordinate = tuple[int, int]

DEFAULT_START = (0, 0)
DEFAULT_DIRECTION = 'E'


class Contraption:
    '''
    Represents the Contraption from this puzzle
    '''
    directions = 'NSEW'
    reflections = {
        '\\': str.maketrans('NSEW', 'WESN'),
        '/': str.maketrans('NSEW', 'EWNS'),
    }

    def __init__(self, path: Path) -> None:
        '''
        Load the input file
        '''
        self.grid = {}
        self.rows = 0
        with path.open() as fh:
            for row_idx, row in enumerate(fh):
                for col_idx, col in enumerate(row.rstrip()):
                    self.grid[(row_idx, col_idx)] = col

        self.rows = max(x[0] for x in self.grid) + 1
        self.cols = max(x[1] for x in self.grid) + 1

    @staticmethod
    def move(
        current: Coordinate,
        direction: str,
    ) -> Coordinate:
        '''
        Return the new position after moving one tile in the specified
        direction.
        '''
        match direction:
            case 'N':
                delta = (-1, 0)
            case 'S':
                delta = (1, 0)
            case 'E':
                delta = (0, 1)
            case 'W':
                delta = (0, -1)
            case _:
                raise ValueError(f'Invalid direction {direction!r}')

        return tuple(a + b for a, b in zip(current, delta))

    def shine_light(
        self,
        tasks: queue.SimpleQueue,
        energized: set[Coordinate],
        start: Coordinate = DEFAULT_START,
        direction: str = DEFAULT_DIRECTION,
    ) -> None:
        '''
        Simulate shining the light through the grid starting at the specified
        position and in the specified direction, returning a set of energized
        coordinates.
        '''
        if direction not in self.directions:
            raise ValueError(f'Invalid direction {direction!r}')

        # If the start point is outside the grid, the light is not in the grid
        if start not in self.grid:
            return

        # Begin by energizing the starting coordinate
        energized.add(start)

        position = None
        while (
            position := start if position is None
            else self.move(position, direction)
        ) in self.grid:
            # Energize the current position
            energized.add(position)
            # Figure out what action (if any) to take
            match self.grid[position]:
                case '-':
                    if direction in 'NS':
                        # Split the beam east and west
                        for new_direction in 'EW':
                            tasks.put({
                                'start': position,
                                'direction': new_direction,
                            })
                        return
                case '|':
                    if direction in 'EW':
                        # Split the beam north and south
                        for new_direction in 'NS':
                            tasks.put({
                                'start': position,
                                'direction': new_direction,
                            })
                        return
                case ('/' | '\\'):
                    # Bounce the beam using the string translation tables
                    # defined as class attributes.
                    direction = direction.translate(
                        self.reflections[self.grid[position]]
                    )
                case '.':
                    # Do nothing
                    pass
                case _:
                    raise ValueError(
                        f'Unhandled grid character {self.grid[position]!r}'
                    )

        return

    def run(
        self,
        start: Coordinate = DEFAULT_START,
        direction: str = DEFAULT_DIRECTION,
    ) -> int:
        '''
        Run a beam of light through the Contraption, returning the number of
        coordinates that are energized.
        '''
        # Initialize the task queue
        tasks = queue.SimpleQueue()
        tasks.put({'start': start, 'direction': direction})
        # Create sets to store the energized coordinates and the permutations
        # we've already called
        energized = set()
        calls = set()

        while not tasks.empty():
            kwargs = tasks.get(block=False)
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
        calls = []
        # Queue up all the coordinates in the top row
        calls.extend(
            {'start': (0, col), 'direction': 'S'}
            for col in range(self.cols)
        )
        # Queue up all the coordinates in the bottom row
        calls.extend(
            {'start': (self.rows - 1, col), 'direction': 'N'}
            for col in range(self.cols)
        )
        # Queue up all the coordinates in the leftmost column
        calls.extend(
            {'start': (row, 0), 'direction': 'E'}
            for row in range(self.rows)
        )
        # Queue up all the coordinates in the rightmost column
        calls.extend(
            {'start': (row, self.cols - 1), 'direction': 'W'}
            for row in range(self.rows)
        )
        return max(self.run(**params) for params in calls)

    def print(self, energized: set[Coordinate]) -> None:
        '''
        Print the grid, with energized coordinates showing as "#" and
        non-energized coordinates showing as "."
        '''
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
    day = 16

    def __init__(self, example: bool = False) -> None:
        '''
        Load the steps
        '''
        super().__init__(example=example)
        self.contraption = Contraption(self.input)

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
    # Run against test data
    aoc = AOC2023Day16(example=True)
    aoc.validate(aoc.part1(), 46)
    aoc.validate(aoc.part2(), 51)
    # Run against actual data
    aoc = AOC2023Day16(example=False)
    aoc.run()
