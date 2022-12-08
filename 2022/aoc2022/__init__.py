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

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the object
        '''
        prefix = 'example' if example else 'day'
        self.input = Path(__file__).parent.parent.joinpath(
            'inputs',
            f'{prefix}{str(self.day).zfill(2)}.txt',
        )
