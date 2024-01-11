#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/19
'''
import collections

# Local imports
from aoc import AOC


class AOC2016Day19(AOC):
    '''
    Day 19 of Advent of Code 2016
    '''
    day: int = 19

    def __init__(self, example: bool = False) -> None:
        '''
        Set the number of elves to be used for the puzzle
        '''
        super().__init__(example=example)
        self.elves = 5 if self.example else 3004953

    def part1(self) -> int:
        '''
        Return the elf who would remain with all the presents.

        Solve this puzzle using the trick from the end of this Numberphile
        video:

            https://youtu.be/uCsD3ZGzMgE

        The title of today's puzzle is a bit of a giveaway that this is a
        version of the Josephus Problem.
        '''
        # A binary representation of a positive int will always begin with
        # "0b1", unless that integer is 0. So we know that we'll always be
        # removing a 1 from the front of the binary number, and adding a 1 to
        # the end of it. Thus, the solution is a simple one-liner, in which we
        # convert the number of elves to binary, ignore the first 3 characters
        # of the resulting string, and add a 1 to the end. Converting this back
        # into an int in base 2 gives us our answer.
        return int(f'{bin(self.elves)[3:]}1', 2)

    def part2(self) -> int:
        '''
        Simulate the present-stealing strategy from Part 2 using a pair of
        deques. Return the number of the elf with all the presents.
        '''
        # Separate the elf numbers into two deques. The first one will contain
        # the first half of the elves, in ascending order. The second will
        # contain the remaining elves, in descending order. If there are an odd
        # number of elves, the first deque will have one more than the second.
        #
        # Considering the 5 elves from the example, the two deques would be
        # configured as follows:
        #
        # first:    1 2 3
        # second:   5 4
        #
        # Consider the case where there are 6 elves. They would be arranged
        # like so:
        #
        # first:    1 2 3
        # second:   6 5 4
        #
        first: collections.deque[int] = collections.deque(
            elf for elf in range(1, (self.elves // 2) + 1)
        )
        second: collections.deque[int] = collections.deque(
            elf for elf in range(self.elves + 1, (self.elves // 2) + 1, -1)
        )

        while second:
            # Moving clockwise around the circle of elves is equivalent to
            # traversing the first deque from beginning to end, and then the
            # second deque from end to beginning. The elf at the beginning of
            # the first queue will _always_ be the one doing the
            # present-stealing (after stealing, the deques will be rotated to
            # put the next present-thief into position; more on that below). If
            # the deques are of equal length, the elf at the end of the second
            # deque will be the one directly across from the elf at the
            # beginning of the first deque. If the deques are _not_ of equal
            # length, then there is no elf directly across from the elf at the
            # beginning of the first deque. The elves at the end of both deques
            # will both be across from the elf at the beginning of the first
            # deque. The one on the "left" will be at the end of the first
            # deque.
            #
            # So, if the deques are imbalanced, steal from the end of the first
            # deque. If they are balanced, steal from the end of the second.
            if len(first) > len(second):
                first.pop()
            else:
                second.pop()

            # We now need to rotate the deques to put the next elf into
            # stealing position. Considering the 5-elf example, elf 3 would
            # have been eliminated above.
            #
            # first:    1 2
            # second:   5 4
            #
            # We need to rotate elf #2 into position. Think of this rotation as
            # a counter-clockwise movement. The result would be:
            #
            # first:    2 4
            # second:   1 5
            #
            # So, how do we express this algorithmically? The 1 needs to move
            # from the front of the first deque to the front of the second one.
            # So we'd need to pop from the front of the first deque, and insert
            # that value at the beginning of the second one.
            second.appendleft(first.popleft())

            # Now our deques look like this:
            #
            # first:    2
            # second:   1 5 4
            #
            # We need to get the 4 from the end of the second deque to the end
            # of the first one. To do this, we'd need to pop from the end of
            # second deque and append to the end of the first one. This would
            # leave us with our desired rotation.
            #
            # first:    2 4
            # second:   1 5
            first.append(second.pop())

            # From here we just repeat the loop, eliminating elves and
            # rotating, until the second deque is empty. Once this is the case,
            # the only remaining elf will be in the first deque.

        # Return the lone remaining elf's number
        return first[0]


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day19(example=True)
    aoc.validate(aoc.part1(), 3)
    aoc.validate(aoc.part2(), 2)
    # Run against actual data
    aoc = AOC2016Day19(example=False)
    aoc.run()
