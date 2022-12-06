'''
Commom Functions
'''
from pathlib import Path


class AOC2022:
    '''
    Base class for Advent of Code 2022
    '''
    # Override this for each day
    day = 0

    def __init__(self):
        '''
        Initialize the object
        '''
        self.input = Path(__file__).parent.parent.joinpath(
            'inputs',
            f'day{str(self.day).zfill(2)}.txt',
        )
