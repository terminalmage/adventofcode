#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/1

--- Day 1: Not Quite Lisp ---

Santa was hoping for a white Christmas, but his weather machine's "snow"
function is powered by stars, and he's fresh out! To save Christmas, he needs
you to collect fifty stars by December 25th.

Collect stars by helping Santa solve puzzles. Two puzzles will be made
available on each day in the Advent calendar; the second puzzle is unlocked
when you complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't
find the right floor - the directions he got are a little confusing. He starts
on the ground floor (floor 0) and then follows the instructions one character
at a time.

An opening parenthesis, (, means he should go up one floor, and a closing
parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will
never find the top or bottom floors.

For example:

    (()) and ()() both result in floor 0.
    ((( and (()(()( both result in floor 3.
    ))((((( also results in floor 3.
    ()) and ))( both result in floor -1 (the first basement level).
    ))) and )())()) both result in floor -3.

To what floor do the instructions take Santa?

--- Part Two ---

Now, given the same instructions, find the position of the first character that
causes him to enter the basement (floor -1). The first character in the
instructions has position 1, the second character has position 2, and so on.

For example:

- ) causes him to enter the basement at character position 1.
- ()()) causes him to enter the basement at character position 5.

What is the position of the character that causes Santa to first enter the basement?

'''
# Local imports
from aoc import AOC


class AOC2015Day1(AOC):
    '''
    Day 1 of Advent of Code 2015
    '''
    day = 1

    def __init__(self, example: bool = False) -> None:
        '''
        Load the instructions
        '''
        super().__init__(example=example)
        with self.input.open() as fh:
            self.instructions = fh.read().strip()

    def part1(self) -> int:
        '''
        Return the floor to which the instructions lead
        '''
        return self.instructions.count('(') - self.instructions.count(')')

    def part2(self) -> int:
        '''
        Return the position where the current floor goes negative
        '''
        floor = 0
        for index, position in enumerate(self.instructions, start=1):
            floor += 1 if position == '(' else -1
            if floor < 0:
                return index
        raise RuntimeError('Failed to find negative floor')


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day1(example=True)
    aoc.validate(aoc.part1(), 3)
    aoc.validate(aoc.part2(), 1)
    # Run against actual data
    aoc = AOC2015Day1(example=False)
    aoc.run()
