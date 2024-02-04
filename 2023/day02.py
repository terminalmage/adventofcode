#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/2
'''
import math
import textwrap

# Local imports
from aoc import AOC


class Cubes:
    '''
    Representation of a collection of cubes
    '''
    colors: frozenset[str] = frozenset({'red', 'green', 'blue'})

    def __init__(self, description: str) -> None:
        '''
        Initialize the object based on the description
        '''
        self.description: str = description.strip()
        count_def: str
        for count_def in self.description.split(','):
            count: str
            color: str
            count, color = count_def.strip().split()
            setattr(self, color, int(count))

    def __getattr__(self, name: str) -> int:
        '''
        Implement fallback if the requested color wasn't part of the
        description used to initialize the object.
        '''
        if name not in self.colors:
            raise AttributeError(
                f'{self.__class__.__name__!r} object has no attribute {name!r}'
            )

        return 0

    def __repr__(self) -> str:
        '''
        String representation of the object
        '''
        return f'Cubes({self.description!r})'

    def __le__(self, other: 'Cubes') -> bool:
        '''
        Define <= operator

        Note that the other operators are not implemented for this type, so
        this is the only operator that can be reliably used for comparisons.
        '''
        return all(
            getattr(self, color) <= getattr(other, color)
            for color in self.colors
        )


class Game:
    '''
    Represents a single game
    '''
    def __init__(self, handfuls: str) -> None:
        '''
        Initialize Cubes objects for each handful
        '''
        self.handfuls: list[Cubes] = [
            Cubes(handful) for handful in handfuls.split(';')
        ]

    def valid(self, bag_contents: Cubes) -> bool:
        '''
        Returns True if all of the handfuls in the game are valid for a bag
        with the specified contents
        '''
        return all(handful <= bag_contents for handful in self.handfuls)

    @property
    def power(self) -> int:
        '''
        Calculate the power of the game
        '''
        return math.prod(
            max(getattr(handful, color) for handful in self.handfuls)
            for color in self.handfuls[0].colors
        )


class AOC2023Day2(AOC):
    '''
    Day 2 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        '''
    )

    validate_part1: int = 8
    validate_part2: int = 2286

    bag_contents: Cubes = Cubes('12 red, 13 green, 14 blue')

    # Set by post_init
    games = None

    def post_init(self) -> None:
        '''
        Initialize the object
        '''
        self.games: dict[int, Game] = {}
        for line in self.input.splitlines():
            game_id: str
            handfuls: str
            game_id, handfuls = line.split(None, 2)[1:]
            self.games[int(game_id.rstrip(':'))] = Game(handfuls)

    def part1(self) -> int:
        '''
        Return the sum of IDs for valid games
        '''
        return sum(
            game_id for game_id, game in self.games.items()
            if game.valid(self.bag_contents)
        )

    def part2(self) -> int:
        '''
        Return the sum of the powers of all games
        '''
        return sum(game.power for game in self.games.values())


if __name__ == '__main__':
    aoc = AOC2023Day2()
    aoc.run()
