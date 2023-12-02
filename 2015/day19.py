#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/19
'''
import functools

# Local imports
from aoc import AOC


class AOC2015Day19(AOC):
    '''
    Day 19 of Advent of Code 2015
    '''
    day = 19

    def __init__(self, example: bool = False) -> None:
        '''
        Load the input data
        '''
        super().__init__(example=example)

        lines = self.input.read_text().splitlines()

        self.molecule = lines[-1]
        self.replacements = []
        for line in lines[:-2]:
            target, _, replacement = line.split()
            self.replacements.append((target, replacement))

    @functools.lru_cache
    def indexes(self, substr: str) -> list[int]:
        '''
        Find indexes of non-overlapping substring match within the desired
        molecule.
        '''
        start = 0
        ret = []

        while (loc := self.molecule.find(substr, start)) != -1:
            ret.append(loc)
            start = loc + len(substr)

        return ret

    def part1(self) -> int:
        '''
        Calculate the number of unique molecules that can be created using the
        specified replacements.
        '''
        molecules = set()

        for target, replacement in self.replacements:
            for index in self.indexes(target):
                left = self.molecule[:index]
                right = self.molecule[index + len(target):]
                molecules.add(f'{left}{replacement}{right}')

        return len(molecules)

    def part2(self) -> int:
        '''
        Calculate the number of steps needed to construct the molecule.
        '''
        molecule = self.molecule
        count = 0
        while molecule != 'e':
            for target, replacement in self.replacements:
                if replacement in molecule:
                    molecule = molecule.replace(replacement, target, 1)
                    count += 1

        return count


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day19(example=True)
    aoc.validate(aoc.part1(), 7)
    # Run against actual data
    aoc = AOC2015Day19(example=False)
    aoc.run()
