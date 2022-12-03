#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/2
'''

from aoc2022 import AOC2022


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


class AOC2022Day2(AOC2022):
    '''
    Base class for Day 2 of Advent of Code 2022
    '''
    day = 2


class AOC2022Day2A(AOC2022Day2):
    '''
    Day 2 of Advent of Code 2022 (first task)
    '''
    def process_input(self):
        '''
        Calculate scores
        '''
        self.games = []
        with self.input.open() as fh:
            for line in fh:
                self.games.append(RockPaperScissors(*line.rstrip('\n').split()))


class AOC2022Day2B(AOC2022Day2):
    '''
    Day 2 of Advent of Code 2022 (second task)
    '''
    day = 2

    def __init__(self):
        super().__init__()

    def process_input(self):
        '''
        Calculate scores
        '''
        self.games = []
        with self.input.open() as fh:
            for line in fh:
                choice1, result = line.rstrip('\n').split()
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

                self.games.append(RockPaperScissors(choice1, choice2))


if __name__ == '__main__':
    aoc1 = AOC2022Day2A()
    answer1 = sum(game.score for game in aoc1.games)
    print(f'Answer 1 (total score): {answer1}')
    aoc2 = AOC2022Day2B()
    answer2 = sum(game.score for game in aoc2.games)
    print(f'Answer 2 (total score): {answer2}')
