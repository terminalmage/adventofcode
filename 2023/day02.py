#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/2
'''
import math

# Local imports
from aoc import AOC


class Cubes:
    '''
    Representation of a collection of cubes
    '''
    colors = frozenset({'red', 'green', 'blue'})

    def __init__(self, description: str) -> None:
        '''
        Initialize the object based on the description
        '''
        self.description = description.strip()
        for count_def in self.description.split(','):
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
        self.handfuls = [Cubes(handful) for handful in handfuls.split(';')]

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
    day = 2

    bag_contents = Cubes('12 red, 13 green, 14 blue')

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the object
        '''
        super().__init__(example=example)
        self.games = {}
        with self.input.open() as fh:
            for line in fh:
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
    # Run against test data
    aoc = AOC2023Day2(example=True)
    aoc.validate(aoc.part1(), 8)
    aoc.validate(aoc.part2(), 2286)
    # Run against actual data
    aoc = AOC2023Day2(example=False)
    aoc.run()
