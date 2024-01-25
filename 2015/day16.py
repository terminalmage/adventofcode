#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/16
'''
import textwrap

# Local imports
from aoc import AOC

# Type hints
SueStat = tuple[str, int]
SueStats = set[SueStat]


class AOC2015Day16(AOC):
    '''
    Day 16 of Advent of Code 2015
    '''
    def post_init(self) -> None:
        '''
        Load the instructions
        '''
        self.sues: dict[int, SueStats] = {}
        for line in self.input.splitlines():
            sue_id: str
            stats: str
            sue_id, stats = line.split(':', 1)
            self.sues[int(sue_id.split()[-1])] = set(
                (item.strip(), int(count.strip()))
                for item, count in (
                    stat.split(':') for stat in stats.split(',')
                )
            )

        self.mystery_sue: SueStats = {
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
        sue_num: int
        stats: SueStats
        for sue_num, stats in self.sues.items():
            if stats.issubset(self.mystery_sue):
                return sue_num

        raise RuntimeError('Failed to find the Mystery Sue')

    def part2(self) -> int:
        '''
        Return the *real* number of the Mystery Sue
        '''
        mystery_sue: dict[str, int] = dict(self.mystery_sue)
        cats: int = mystery_sue.pop('cats')
        trees: int = mystery_sue.pop('trees')
        pomeranians: int = mystery_sue.pop('pomeranians')
        goldfish: int = mystery_sue.pop('goldfish')
        mystery_sue_stats: SueStats = set(mystery_sue.items())

        for sue_num, stats in self.sues.items():
            stats_dict: dict[str, int] = dict(stats)
            sue_cats: int | None = stats_dict.pop('cats', None)
            sue_trees: int | None = stats_dict.pop('trees', None)
            sue_pomeranians: int | None = stats_dict.pop('pomeranians', None)
            sue_goldfish: int | None = stats_dict.pop('goldfish', None)

            if set(stats_dict.items()).issubset(mystery_sue_stats):
                stats_dict: dict[str, int] = dict(stats)
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
    aoc = AOC2015Day16()
    aoc.run()
