#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/9
'''
import queue
import textwrap

# Local imports
from aoc import AOC


class AOC2017Day9(AOC):
    '''
    Day 9 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        {}
        {{{}}}
        {{},{}}
        {{{},{},{{}}}}
        {<a>,<a>,<a>,<a>}
        {{<ab>},{<ab>},{<ab>},{<ab>}}
        {{<!!>},{<!!>},{<!!>},{<!!>}}
        {{<a!>},{<a!>},{<a!>},{<ab>}}
        '''
    )

    validate_part1: int = 50

    def post_init(self) -> None:
        '''
        Load the puzzle input and process the stream
        '''
        # Total score of all groups in all streams (NOTE: the example input has
        # multiple lines of streams, but the puzzle input is one long line)
        self.score: int = 0
        # Number of non-canceled characters within a garbage block
        self.garbage: int = 0

        stream: str
        for stream in self.input.splitlines():

            # Current position within the stream
            index: int = 0
            # Whether or not our current position is within a block of garbage
            garbage: bool = False
            # Depth of current group (0 if not presently in a group)
            depth: int = 0
            # Track the depth of nested groups so that they can be assigned the
            # correct scores.
            group_score: queue.LifoQueue[int] = queue.LifoQueue()

            while index < len(stream):
                cur: str = stream[index]

                if garbage and cur not in '!>':
                    self.garbage += 1

                match cur:
                    case '!':
                        # Each iteration through the loop we increment the index to
                        # process the next character. However, when the current
                        # position is a negation character, we need to advance one
                        # more position (to ignore the character after the current
                        # position).
                        index += 1

                    case '<':
                        # Beginning of garbage block
                        garbage = True

                    case '>':
                        if garbage:
                            # End of garbage block
                            garbage = False

                    case '{':
                        if not garbage:
                            # Beginning of a group. Increase the depth and toss
                            # it onto the stack.
                            depth += 1
                            group_score.put(depth)

                    case '}':
                        if not garbage:
                            # End of a group. Decrease the depth and grab the
                            # score off the top of the stack, adding it to the
                            # total.
                            depth -= 1
                            self.score += group_score.get()

                index += 1

    def part1(self) -> int:
        '''
        Return the score based on the criteria defined in the puzzle
        '''
        return self.score

    def part2(self) -> int:
        '''
        Return the number of uncancelled characters within garbage blocks
        '''
        return self.garbage


if __name__ == '__main__':
    aoc = AOC2017Day9()
    aoc.run()
