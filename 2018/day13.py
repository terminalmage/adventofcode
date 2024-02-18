#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/13
'''
from __future__ import annotations
import itertools
import textwrap
from dataclasses import dataclass, field

# Local imports
from aoc import AOC, TupleMixin, XY, directions


@dataclass
class Cart(TupleMixin):
    '''
    Stores information about a single cart
    '''
    position: XY
    direction: XY
    turns: itertools.cycle = field(init=False)

    def __post_init__(self) -> None:
        '''
        Initialize the turns attribute
        '''
        # Given the "directions" namedtuple, reducing the index by 1 is
        # equivalent to a left turn, and increasing by 1 is equivalent to a
        # right turn. So this attribute will produce a repeating sequence of
        # left, straight, right when next() is used to get a value from it.
        self.turns = itertools.cycle((-1, 0, 1))

    def move(self) -> None:
        '''
        Move the cart once
        '''
        self.position = self.tuple_add(self.position, self.direction)

    def __lt__(self, other: Cart) -> bool:
        '''
        Implement < operator to make instances sortable
        '''
        return self.position < other.position

class Track:
    '''
    Stores track diagram and simulates cart movement
    '''
    corners: str = r'\/'
    rails: str = '|-+'

    def __init__(self, track_map: str) -> None:
        '''
        Load the track map and find all of the carts
        '''
        self.map: dict[XY, str] = {}
        self.initial_cart_positions: list[tuple[XY, XY]] = []
        self.carts: list[Cart] = []

        # Type hints
        row: int
        col: int
        line: str
        tile: str

        for row, line in enumerate(track_map.splitlines()):
            for col, tile in enumerate(line):
                if tile in self.corners or tile in self.rails:
                    self.map[row, col] = tile
                else:
                    direction: XY
                    match tile:
                        case ' ':
                            # Not part of the track and not a cart
                            continue
                        case '^':
                            direction = directions.NORTH
                            self.map[row, col] = '|'
                        case 'v':
                            direction = directions.SOUTH
                            self.map[row, col] = '|'
                        case '<':
                            direction = directions.WEST
                            self.map[row, col] = '-'
                        case '>':
                            direction = directions.EAST
                            self.map[row, col] = '-'
                        case _:
                            raise ValueError(
                                f'Unexpected character {tile!r} found at '
                                f'row {row + 1}, col {col + 1}'
                            )
                    self.initial_cart_positions.append(((row, col), direction))

    def reset(self) -> None:
        '''
        Reset the carts to their initial positions
        '''
        self.carts[:] = [
            Cart(*pos)
            for pos in self.initial_cart_positions
        ]
        assert self.carts

    def turn_cart(self, cart: Cart) -> None:
        '''
        Handle turning the cart if it has reached a corner/intersection
        '''
        tile: str = self.map[cart.position]
        if tile in self.corners:
            # Turn the cart
            match cart.direction:
                case directions.NORTH:
                    cart.direction = directions.EAST \
                        if tile == '/' \
                        else directions.WEST
                case directions.SOUTH:
                    cart.direction = directions.WEST \
                        if tile == '/' \
                        else directions.EAST
                case directions.WEST:
                    cart.direction = directions.SOUTH \
                        if tile == '/' \
                        else directions.NORTH
                case directions.EAST:
                    cart.direction = directions.NORTH \
                        if tile == '/' \
                        else directions.SOUTH

        elif tile == '+':
            # Handle turning at an intersection. Get the current index
            # and add the offset from the cart's "turns" attribute,
            # then take the remainder from dividing 4.
            index: int = directions.index(cart.direction) + next(cart.turns)
            cart.direction = directions[index % 4]

    def find_first_crash(self) -> str:
        '''
        Run the carts along the track until a crash happens. Return the
        location of the crash.
        '''
        self.reset()

        while True:
            self.carts.sort()
            positions: set[XY] = set()
            cart: Cart
            for cart in self.carts:
                cart.move()
                if cart.position in positions:
                    # Crash! Return the position as col,row (i.e. reversed from
                    # how these objects store them).
                    return ','.join(str(n) for n in reversed(cart.position))
                positions.add(cart.position)
                self.turn_cart(cart)

    def last_cart_standing(self) -> str:
        '''
        Run the carts until all have collided and been removed from the track.
        Return the position of the last cart to remain.
        '''
        self.reset()

        while True:
            # Since I implmented the carts as objects (to make tracking
            # position, direction, and turns easier), create a mapping of the
            # positions of the carts which we will update as they move and use
            # to detect collisions. This prevents repeated iteration over the
            # list of carts to find one with a matching position.
            positions: dict[XY, int] = {
                cart.position: index
                for index, cart in enumerate(self.carts)
            }
            # Holds the indexes of any carts which need to be removed
            to_remove: set[int] = set()

            # Move each cart in the order of their current position
            cart: Cart
            for index, cart in enumerate(self.carts):

                if index in to_remove:
                    # This cart was run into earlier this round
                    continue

                # Cart is about to move, remove it from the positions dict
                positions.pop(cart.position)
                # Move the cart one space in its current direction
                cart.move()

                # Check for collision
                if cart.position in positions:
                    # Collision found, mark both carts for removal
                    to_remove.add(positions.pop(cart.position))
                    to_remove.add(index)
                else:
                    # No collision. Update the position for this cart
                    positions[cart.position] = index
                    self.turn_cart(cart)

            # Remove any carts which were marked for removal
            if to_remove:
                self.carts = [
                    cart for index, cart in enumerate(self.carts)
                    if index not in to_remove
                ]

            # After movement/removal, positions may have changed, re-sort the
            # carts so that they move in the correct order in the next round.
            self.carts.sort()

            if len(self.carts) == 1:
                # Return the position of this final cart
                return ','.join(str(n) for n in reversed(self.carts[0].position))

            if not self.carts:
                raise RuntimeError('All carts eliminated')


class AOC2018Day13(AOC):
    '''
    Day 13 of Advent of Code 2018
    '''
    example_data_part1: str = textwrap.dedent(
        r'''
        /->-\
        |   |  /----\
        | /-+--+-\  |
        | | |  | v  |
        \-+-/  \-+--/
          \------/
        '''
    )

    example_data_part2: str = textwrap.dedent(
        r'''
        />-<\
        |   |
        | /<+-\
        | | | v
        \>+</ |
          |   ^
          \<->/
        '''
    )

    validate_part1: str = '7,3'
    validate_part2: str = '6,4'

    def part1(self) -> str:
        '''
        Find the location of the first crash
        '''
        track = Track(self.input_part1)
        return track.find_first_crash()

    def part2(self) -> str:
        '''
        Find the last cart standing
        '''
        track = Track(self.input_part2)
        return track.last_cart_standing()


if __name__ == '__main__':
    aoc = AOC2018Day13()
    aoc.run()
