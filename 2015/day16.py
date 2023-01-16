#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/16
'''
# Local imports
from aoc import AOC


class AOC2015Day16(AOC):
    '''
    Day 14 of Advent of Code 2015
    '''
    day = 16

    def __init__(self, example: bool = False) -> None:
        '''
        Load the instructions
        '''
        super().__init__(example=example)

        self.sues = {}
        with self.input.open() as fh:
            for line in fh:
                sue_id, stats = line.split(':', 1)
                self.sues[int(sue_id.split()[-1])] = set(
                    (item.strip(), int(count.strip()))
                    for item, count in (
                        stat.split(':') for stat in stats.split(',')
                    )
                )

        self.mystery_sue = {
            ('children', 3),
            ('cats', 7),
            ('samoyeds', 2),
            ('pomeranians', 3),
            ('akitas', 0),
            ('vizslas', 0),
            ('goldfish', 5),
            ('trees', 3),
            ('cars', 2),
            ('perfumes', 1),
        }

    def part1(self) -> int:
        '''
        Return the number of the Mystery Sue
        '''
        for sue_num, stats in self.sues.items():
            if stats.issubset(self.mystery_sue):
                return sue_num

        raise RuntimeError('Failed to find the Mystery Sue')

    def part2(self) -> int:
        '''
        Return the *real* number of the Mystery Sue
        '''
        mystery_sue = dict(self.mystery_sue)
        cats = mystery_sue.pop('cats')
        trees = mystery_sue.pop('trees')
        pomeranians = mystery_sue.pop('pomeranians')
        goldfish = mystery_sue.pop('goldfish')
        mystery_sue_stats = set(mystery_sue.items())

        for sue_num, stats in self.sues.items():
            stats_dict = dict(stats)
            sue_cats = stats_dict.pop('cats', None)
            sue_trees = stats_dict.pop('trees', None)
            sue_pomeranians = stats_dict.pop('pomeranians', None)
            sue_goldfish = stats_dict.pop('goldfish', None)

            if set(stats_dict.items()).issubset(mystery_sue_stats):
                stats_dict = dict(stats)
                if sue_cats is not None and sue_cats <= cats:
                    continue
                if sue_trees is not None and sue_trees <= trees:
                    continue
                if sue_pomeranians is not None and sue_pomeranians >= pomeranians:
                    continue
                if sue_goldfish is not None and sue_goldfish >= goldfish:
                    continue

                return sue_num

        raise RuntimeError('Failed to find the Mystery Sue')


if __name__ == '__main__':
    # Run against actual data
    aoc = AOC2015Day16(example=False)
    aoc.run()
