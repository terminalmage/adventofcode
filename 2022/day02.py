#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/2
'''
import textwrap

# Local imports
from aoc import AOC

WINS: dict[str, str] = {
    'rock': 'paper',
    'paper': 'scissors',
    'scissors': 'rock',
}
LOSES: dict[str, str] = {val: key for key, val in WINS.items()}


def normalize(value: str) -> str:
    '''
    Translate the input from the strategy guide to the corresponding choice
    '''
    match value:
        case 'A' | 'X':
            return 'rock'
        case 'B' | 'Y':
            return 'paper'
        case 'C' | 'Z':
            return 'scissors'
        case _:
            raise ValueError(f'Invalid input: {value}')


class RockPaperScissors:
    '''
    Class to represent the result of a single game of rock, paper, scissors
    '''
    def __init__(self, choice1: str, choice2: str):
        self.choice1: str = choice1
        self.choice2: str = choice2

    def __repr__(self) -> str:
        '''
        Define repr() output for class
        '''
        return (
            f'RockPaperScissors(choice1={self.choice1!r}, '
            f'choice2={self.choice2!r}, result={self.result}, '
            f'score={self.score})'
        )

    def __calculate_score(self):
        '''
        Calculate the score for this round
        '''
        scores: dict[str, int] = {
            'rock': 1,
            'paper': 2,
            'scissors': 3,
        }
        # pylint: disable=attribute-defined-outside-init
        # Determine result
        self.result: str
        self.score: int
        if self.choice2 == self.choice1:
            self.result = 'draw'
            self.score = 3
        elif self.choice2 == WINS[self.choice1]:
            self.result = 'win'
            self.score = 6
        else:
            self.result = 'loss'
            self.score = 0
        # pylint: enable=attribute-defined-outside-init

        # Add in score for your choice (i.e. choice2)
        self.score += scores[self.choice2]

    @property
    def choice1(self) -> str:
        '''
        Return the first choice
        '''
        return self.__choice1

    @property
    def choice2(self) -> str:
        '''
        Return the second choice
        '''
        return self.__choice2

    @staticmethod
    def __validate(value: str) -> str:
        '''
        Validate the value for this choice
        '''
        match value:
            case 'rock' | 'paper' | 'scissors':
                return value
            case _:
                return normalize(value)

    @choice1.setter
    def choice1(self, value: str) -> None:
        '''
        Set the first choice
        '''
        self.__choice1: str = self.__validate(value)
        if hasattr(self, 'choice2'):
            self.__calculate_score()

    @choice2.setter
    def choice2(self, value: str) -> None:
        '''
        Set the second choice
        '''
        self.__choice2: str = self.__validate(value)
        if hasattr(self, 'choice1'):
            self.__calculate_score()


class AOC2022Day2(AOC):
    '''
    Day 2 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
        A Y
        B X
        C Z
        '''
    )

    validate_part1: int = 15
    validate_part2: int = 12

    def part1(self) -> int:
        '''
        Calculate the total score, assuming that the guide is describing which
        choices should be made by both parties
        '''
        return sum(
            game.score for game in (
                RockPaperScissors(*line.split())
                for line in self.input.splitlines()
            )
        )

    def part2(self) -> int:
        '''
        Calculate the total score, assuming that the second column of each line
        in the guide instructs you whether to win, lose, or draw
        '''
        # Type hints
        choice1: str
        choice2: str
        result: str

        total: int = 0

        for line in self.input.splitlines():
            choice1, result = line.split()
            choice1 = normalize(choice1)
            match result:
                case 'X':
                    # Need to lose
                    choice2 = LOSES[choice1]
                case 'Y':
                    # Need to draw
                    choice2 = choice1
                case 'Z':
                    # Need to win
                    choice2 = WINS[choice1]
                case _:
                    raise ValueError(f'Invalid result: {result!r}')

            total += RockPaperScissors(choice1, choice2).score

        return total


if __name__ == '__main__':
    aoc = AOC2022Day2()
    aoc.run()
