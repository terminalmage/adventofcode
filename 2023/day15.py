#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/15
'''
import textwrap
from collections import defaultdict

# Local imports
from aoc import AOC


class AOC2023Day15(AOC):
    '''
    Day 15 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        '''
    )

    validate_part1: int = 1320
    validate_part2: int = 145

    # Set by post_init
    steps = None

    def post_init(self) -> None:
        '''
        Load the steps
        '''
        self.steps: tuple[str, ...] = tuple(self.input.split(','))

    @staticmethod
    def hash(text: str) -> int:
        '''
        Calculate the hash for a given string
        '''
        ret: int = 0
        char: str
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
        boxes: defaultdict[str, dict[str, int]] = defaultdict(dict)
        step: str
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
    aoc = AOC2023Day15()
    aoc.run()
