#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/9
'''
import textwrap

# Local imports
from aoc import AOC

# Type hints
Layers = list[list[int]]


class AOC2023Day9(AOC):
    '''
    Day 9 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        '''
    )

    validate_part1: int = 114
    validate_part2: int = 2

    # Set by post_init
    sequences = None

    def post_init(self) -> None:
        '''
        Load sequences from input file
        '''
        self.sequences: tuple[tuple[int, ...], ...] = tuple(
            tuple(int(item) for item in line.split())
            for line in self.input.splitlines()
        )

    @staticmethod
    def map_sequence(seq: tuple[int]) -> Layers:
        '''
        Given a sequence of integers, return a map of differences that can be
        used to extrapolate the next/previous item(s) in the sequence.
        '''
        # Start with the sequence passed in
        layers: Layers = [list(seq)]

        # Generate all additional layers until the result is a layer
        # containing all zeroes.
        while set(prev_layer := layers[-1]) != {0}:
            layers.append(
                [
                    prev_layer[i+1] - prev_layer[i]
                    for i in range(len(prev_layer) - 1)
                ]
            )

        return layers

    def solve_part1(self, seq: tuple[int]) -> int:
        '''
        Determine the next item in the sequence
        '''
        # Map out all the differences
        layers: Layers = self.map_sequence(seq)

        # Calculate the next item in each layer, from the bottom up. Start by
        # adding another zero to the last layer.
        layers[-1].append(0)
        index: int
        for index in range(len(layers) - 2, -1, -1):
            layers[index].append(layers[index][-1] + layers[index + 1][-1])

        # The last element of the first layer should now contain the next item
        # in the sequence.
        return layers[0][-1]

    def solve_part2(self, seq: tuple[int]) -> int:
        '''
        Determine the previous item in the sequence
        '''
        # Map out all the differences
        layers: Layers = self.map_sequence(seq)

        # Calculate the previous item in each layer, from the bottom up. Start
        # by inserting another zero into the last layer.
        layers[-1].insert(0, 0)
        index: int
        for index in range(len(layers) - 2, -1, -1):
            layers[index].insert(0, layers[index][0] - layers[index + 1][0])

        # The first element of the first layer should now contain the previous
        # item in the sequence.
        return layers[0][0]

    def part1(self) -> int:
        '''
        Return the sum of the next numbers in each sequence
        '''
        return sum(self.solve_part1(seq) for seq in self.sequences)

    def part2(self) -> int:
        '''
        Return the sum of the previous numbers in each sequence
        '''
        return sum(self.solve_part2(seq) for seq in self.sequences)


if __name__ == '__main__':
    aoc = AOC2023Day9()
    aoc.run()
