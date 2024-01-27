#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/19
'''
import string
import textwrap
from collections.abc import Generator

# Local imports
from aoc import AOC, Grid, XY


class PacketRoute(Grid):
    '''
    Grid subclass which includes functions for traversing a routing diagram
    from the puzzle input
    '''
    def follow(self, all_steps: bool = False) -> Generator[str, None, None]:
        '''
        Follow the route. If all_steps is True, yield each step. Otherwise,
        yield just the uppercase letters.
        '''
        prev_position: XY = self.find('|')
        direction: XY = self.directions.SOUTH

        if all_steps:
            yield '|'

        # The letters we may encounter while traversing the pipe
        letters: frozenset[str] = frozenset(string.ascii_uppercase)
        # Tube characters (including bends)
        tube_chars: frozenset[str] = frozenset('-|+')
        # Valid characters that can come after a bend include any of the above,
        # with the exception of another turn.
        after_bend = tube_chars | letters - {'+'}

        while True:
            position: XY = self.tuple_add(prev_position, direction)

            try:
                tile: str = self[position]
            except IndexError:
                # Route has exited grid
                break

            if tile in letters:
                # Letter character reached
                yield tile
            elif tile not in tube_chars:
                # Route has terminated
                break
            else:
                if all_steps:
                    yield tile

                # Route continues. Check for bends and detect new direction.
                if tile == '+':
                    # Bends are 90-degree turns (i.e. you do not continue
                    # straight through them). The self.directions namedtuple is
                    # in clockwise order, so a left or right turn is the same
                    # as adding 1 to (or subtracting 1 from) the tuple index of
                    # the current direction, mod the number of directions (4).
                    cur_index: int = self.directions.index(direction)
                    for offset in (-1, 1):
                        new_idx: int = (cur_index + offset) % 4
                        new_direction: XY = self.directions[new_idx]
                        try:
                            new_tile: str = self[self.tuple_add(position, new_direction)]
                        except IndexError:
                            # Turning in this direction would exit the bounds
                            # of the grid.
                            continue
                        if new_tile in after_bend:
                            direction = new_direction
                            break
                    else:
                        # Convert the current direction to its attribute name
                        # (NORTH, EAST, etc.) and convert to lowercase.
                        dir_human: str = self.directions._fields[cur_index].lower()
                        raise ValueError(
                            f'Failed to detect new direction after entering '
                            f'{position} while moving {dir_human}.'
                        )

            prev_position = position


class AOC2017Day19(AOC):
    '''
    Day 19 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
             |
             |  +--+
             A  |  C
         F---|----E|--+
             |  |  |  D
             +B-+  +--+
        '''
    )

    validate_part1: str = 'ABCDEF'
    validate_part2: int = 38

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.route: PacketRoute = PacketRoute(self.input)

    def part1(self) -> str:
        '''
        Return the letters encountered while traversing the route, in the order
        they were encountered.
        '''
        return ''.join(self.route.follow())

    def part2(self) -> int:
        '''
        Return the total number of steps traversed.
        '''
        return len(''.join(self.route.follow(all_steps=True)))


if __name__ == '__main__':
    aoc = AOC2017Day19()
    aoc.run()
