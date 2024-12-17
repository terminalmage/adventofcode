#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/16
'''
import heapq
import textwrap
from collections.abc import Sequence
from typing import Literal

# Local imports
from aoc import AOC, Grid, XY, directions

WALL: Literal['#'] = '#'

# Type hints
DirectionIndex = int  # 0 - 3, from directions namedtuple
Score = int
State = tuple[XY, DirectionIndex]
States = dict[State, Score]


class Maze(Grid):
    '''
    Simulate the warehouse and track contents
    '''
    opposites: dict[XY, XY] = {
        directions.NORTH: directions.SOUTH,
        directions.SOUTH: directions.NORTH,
        directions.WEST: directions.EAST,
        directions.EAST: directions.WEST,
    }

    def __init__(self, data: str) -> None:
        '''
        Initialize the Maze object and find the start and end points
        '''
        super().__init__(data)
        self.start: XY = self.find('S')
        self.end: XY = self.find('E')

    def dijkstra(self, starts: Sequence[State]) -> States:
        '''
        Use Dijkstra to walk paths and get scores along the way
        '''
        q: list[tuple[Score, XY, DirectionIndex]] = []
        states: States = {}

        for start in starts:
            states[start] = 0
            heapq.heappush(q, (0, *start))

        score: Score
        pos: XY
        dir_index: DirectionIndex
        while q:
            score, pos, dir_index = heapq.heappop(q)
            state: State = (pos, dir_index)

            if score > states[state]:
                # This is a less-optimal path than what we already have for
                # this position and direction. No need to pursue it further.
                continue

            if state not in states:
                states[state] = score

            direction: XY = directions[dir_index]
            new_pos: XY = self.tuple_add(pos, direction)
            new_state: State = (new_pos, dir_index)

            if (
                new_pos in self
                and self[new_pos] != WALL
                and (
                    new_state not in states
                    or states[new_state] > (score + 1)
                )
            ):
                states[new_state] = score + 1
                heapq.heappush(q, (score + 1, new_pos, dir_index))

            turn: int
            for turn in (-1, 1):
                new_dir_index: int = (dir_index + turn) % 4
                new_state: State = (pos, new_dir_index)
                if (
                    new_state not in states
                    or states[new_state] > (score + 1000)
                ):
                    states[new_state] = score + 1000
                    heapq.heappush(q, (score + 1000, *new_state))

        return states


class AOC2024Day16(AOC):
    '''
    Day 16 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        #################
        #...#...#...#..E#
        #.#.#.#.#.#.#.#.#
        #.#.#.#...#...#.#
        #.#.#.#.###.#.#.#
        #...#.#.#.....#.#
        #.#.#.#.#.#####.#
        #.#...#.#.#.....#
        #.#.#####.#.###.#
        #.#.#.......#...#
        #.#.###.#####.###
        #.#.#...#.....#.#
        #.#.#.#####.###.#
        #.#.#.........#.#
        #.#.#.#########.#
        #S#.............#
        #################
        '''
    )

    validate_part1: int = 11048
    validate_part2: int = 64

    # Set by post_init
    maze = None

    def post_init(self) -> None:
        '''
        Load the input data into a Maze object
        '''
        self.maze: Maze = Maze(self.input)

    def best_score(self, states: States) -> int:
        '''
        Return the best maze score from the given graph of states
        '''
        best: int = int(1e9)

        pos: XY
        dir_index: int
        for pos, dir_index in states:
            if pos == self.maze.end:
                best = min(best, states[(pos, dir_index)])

        return best

    def part1(self) -> int:
        '''
        Return the best (i.e lowest) possible score for a path from the start
        to the exit.
        '''
        start_state: State = (self.maze.start, directions.index(directions.EAST))
        states: States = self.maze.dijkstra(starts=[start_state])
        return self.best_score(states)

    def part2(self) -> int:
        '''
        There is more than one path which has the highest possible score.
        Return the number of unique coordinates which are part of these paths.
        '''
        # Get the best possible paths in both directions, going from start to
        # end and from end to start.
        start_state: State = (self.maze.start, directions.index(directions.EAST))
        forward_states: States = self.maze.dijkstra(starts=[start_state])
        reverse_states: States = self.maze.dijkstra(
            starts=[(self.maze.end, x) for x in range(4)]
        )

        best_score: int = self.best_score(forward_states)
        on_optimal_path: set[XY] = set()

        # A coordinate is on one of the optimal paths if the score for that
        # coordinate in both the forward and backward traversals combine to
        # equal the best possible score.
        state: State
        for state in forward_states:  # pylint: disable=consider-using-dict-items
            # Flip the direction for comparison purposes
            reverse_state = (state[0], (state[1] + 2) % 4)
            if (
                reverse_state in reverse_states
                and (forward_states[state] + reverse_states[reverse_state] == best_score)
            ):
                on_optimal_path.add(state[0])

        return len(on_optimal_path)


if __name__ == '__main__':
    aoc = AOC2024Day16()
    aoc.run()
