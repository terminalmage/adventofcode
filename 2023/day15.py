#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/15
'''
import collections

# Local imports
from aoc import AOC


class AOC2023Day15(AOC):
    '''
    Day 15 of Advent of Code 2023
    '''
    day = 15

    def __init__(self, example: bool = False) -> None:
        '''
        Load the steps
        '''
        super().__init__(example=example)
        self.steps = tuple(self.input.read_text().rstrip().split(','))

    @staticmethod
    def hash(text: str) -> int:
        '''
        Calculate the hash for a given string
        '''
        ret = 0
        for char in text:
            ret = ((ret + ord(char)) * 17) % 256
        return ret

    def part1(self) -> int:
        '''
        Return sum of hashes for each step
        '''
        return sum(self.hash(step) for step in self.steps)

    def part2(self) -> int:
        '''
        Calculate and return the lens' focusing power
        '''
        boxes = collections.defaultdict(dict)
        for step in self.steps:
            # Operations are defined in one of two formats:
            #
            # 1. label=focal_length (hash label and add to hash's box)
            # 2. label-             (hash label and remove from hash's box)
            #
            # Since the operations in format 1 always have an equals sign in
            # them, and never end in a dash, and the operations in format 2
            # never have an equals sign, we can remove trailing dashes from
            # each operation. If the result has an equals sign in it, then we
            # know it's format 1. If it does not, then it's format 2.
            match step.rstrip('-').split('='):
                case [label, focal_length]:
                    # We can use a dict instead of a list of label/focal length
                    # pairs, because dict iteration order == insertion order.
                    # Therefore, even as items are replaced/removed, when we
                    # enumerate the box's values, they will be in slot order.
                    boxes[self.hash(label)][label] = int(focal_length)
                case [label]:
                    boxes[self.hash(label)].pop(label, None)
                case _:
                    raise ValueError(f'Invalid operation {step!r}')

        return sum(
            sum(
                (box_num + 1) * slot * focal_length
                for slot, focal_length in enumerate(boxes[box_num].values(), 1)
            )
            for box_num in range(256)
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day15(example=True)
    aoc.validate(aoc.part1(), 1320)
    aoc.validate(aoc.part2(), 145)
    # Run against actual data
    aoc = AOC2023Day15(example=False)
    aoc.run()
