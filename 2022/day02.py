#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/2
'''
# Local imports
from aoc import AOC

WINS = {
    'rock': 'paper',
    'paper': 'scissors',
    'scissors': 'rock',
}
LOSES = {val: key for key, val in WINS.items()}


def normalize(value: str):
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
    def __init__(self, choice1, choice2):
        self.choice1 = choice1
        self.choice2 = choice2

    def __repr__(self):
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
        scores = {
            'rock': 1,
            'paper': 2,
            'scissors': 3,
        }
        # pylint: disable=attribute-defined-outside-init
        # Determine result
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
    def __validate(value: str):
        '''
        Validate the value for this choice
        '''
        match value:
            case 'rock' | 'paper' | 'scissors':
                return value
            case _:
                return normalize(value)

    @choice1.setter
    def choice1(self, value: str):
        '''
        Set the first choice
        '''
        self.__choice1 = self.__validate(value)
        if hasattr(self, 'choice2'):
            self.__calculate_score()

    @choice2.setter
    def choice2(self, value: str):
        '''
        Set the second choice
        '''
        self.__choice2 = self.__validate(value)
        if hasattr(self, 'choice1'):
            self.__calculate_score()


class AOC2022Day2(AOC):
    '''
    Day 2 of Advent of Code 2022
    '''
    day = 2

    def part1(self) -> int:
        '''
        Calculate the total score, assuming that the guide is describing which
        choices should be made by both parties
        '''
        with self.input.open() as fh:
            return sum(
                game.score for game in (
                    RockPaperScissors(*line.rstrip().split())
                    for line in fh
                )
            )

    def part2(self) -> int:
        '''
        Calculate the total score, assuming that the second column of each line
        in the guide instructs you whether to win, lose, or draw
        '''
        total = 0

        with self.input.open() as fh:
            for line in fh:
                choice1, result = line.rstrip().split()
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
    # Run against test data
    aoc = AOC2022Day2(example=True)
    aoc.validate(aoc.part1(), 15)
    aoc.validate(aoc.part2(), 12)
    # Run against actual data
    aoc = AOC2022Day2(example=False)
    aoc.run()
