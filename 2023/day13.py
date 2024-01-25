#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/13
'''
import textwrap

# Local imports
from aoc import AOC

# Typing shortcuts
Pattern = tuple[str, ...]


class AOC2023Day13(AOC):
    '''
    Day 13 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        '''
    )

    validate_part1: int = 405
    validate_part2: int = 400

    def post_init(self) -> None:
        '''
        Initialize the object
        '''
        self.patterns: tuple[Pattern] = tuple(
            tuple(pattern.splitlines())
            for pattern in self.input.split('\n\n')
        )

    @staticmethod
    def find_reflection(pattern: Pattern, smudges: int = 0) -> int:
        '''
        Calculate the reflection value for the pattern with the specified
        amount of "smudges". A "smudge" is a single point that, if flipped,
        would result in an exact reflection. Zero smudges (the default) is
        equivalent to an exact reflection with no differences.

        Patterns are stored as sequences of lines of text. Equally-sized slices
        of lines are compared at a time, for example lines 1 and 2, 1-2 and
        3-4, 1-3 and 4-6, etc. While comparing, the first set of lines are
        reversed, so that 3 is paired with 4, 2 is paired with 5, 1 is paired
        with 6...

        Python's zip() function is used to pair these line slices. Running
        zip() again on each line pair produces pairs of columns. From there we
        can count the number of columns that differ, and then add up the number
        differences for each line pair. If the result matches the amount of
        desired "smudges", then we've found the point of reflection. The value
        for this reflection is size of the line slices that were being
        compared.
        '''
        index: int
        for index in range(1, len(pattern)):
            if sum(
                sum(col1 != col2 for col1, col2 in zip(*zipped))
                for zipped in zip(
                    pattern[index - 1::-1],
                    pattern[index:],
                )
            ) == smudges:
                # Because we started with index = 1, the size of the line
                # slices during a given loop iteration is equal to the index.
                return index

        return 0

    @staticmethod
    def rotate(pattern: Pattern) -> Pattern:
        '''
        Given a Pattern, return a new Pattern rotated 90 degrees clockwise
        '''
        num_rows: len = len(pattern)
        num_cols: len = len(pattern[0])
        return tuple(
            ''.join(
                pattern[col_idx][row_idx]
                for col_idx in range(num_rows - 1, -1, -1)
            ) for row_idx in range(num_cols)
        )

    def solve(self, pattern: Pattern, smudges: int = 0) -> int:
        '''
        Find the reflection value for the pattern. Try horizontal comparison
        first. If that doesn't work, rotate the pattern clockwise and repeat
        the attempt.
        '''
        val: int = self.find_reflection(pattern, smudges)
        if val:
            # Horizontal reflections have a 100x multiplier
            return 100 * val
        return self.find_reflection(self.rotate(pattern), smudges)

    def part1(self) -> int:
        '''
        Solve for Part 1
        '''
        return sum(self.solve(pattern) for pattern in self.patterns)

    def part2(self) -> int:
        '''
        Solve for Part 2
        '''
        return sum(self.solve(pattern, 1) for pattern in self.patterns)


if __name__ == '__main__':
    aoc = AOC2023Day13()
    aoc.run()
