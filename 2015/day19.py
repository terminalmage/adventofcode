#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/19
'''
import functools
import textwrap

# Local imports
from aoc import AOC


@functools.cache
def indexes(molecule: str, substr: str) -> list[int]:
    '''
    Find indexes of non-overlapping substring match within the desired
    molecule.
    '''
    start: int = 0
    ret: list[int] = []

    while (loc := molecule.find(substr, start)) != -1:
        ret.append(loc)
        start = loc + len(substr)

    return ret


class AOC2015Day19(AOC):
    '''
    Day 19 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        H => HO
        H => OH
        O => HH

        HOHOHO
        '''
    )

    validate_part1: int = 7

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        lines = self.input.splitlines()

        self.molecule: str = lines[-1]
        self.replacements: list[tuple[str, str]] = []
        for line in lines[:-2]:
            target, _, replacement = line.split()
            self.replacements.append((target, replacement))

    def part1(self) -> int:
        '''
        Calculate the number of unique molecules that can be created using the
        specified replacements.
        '''
        molecules: set[str] = set()

        for target, replacement in self.replacements:
            for index in indexes(self.molecule, target):
                left = self.molecule[:index]
                right = self.molecule[index + len(target):]
                molecules.add(f'{left}{replacement}{right}')

        return len(molecules)

    def part2(self) -> int:
        '''
        Calculate the number of steps needed to construct the molecule.
        '''
        molecule: str = self.molecule
        count: int = 0
        while molecule != 'e':
            target: str
            replacement: str
            for target, replacement in self.replacements:
                if replacement in molecule:
                    molecule = molecule.replace(replacement, target, 1)
                    count += 1

        return count


if __name__ == '__main__':
    aoc = AOC2015Day19()
    aoc.run()
