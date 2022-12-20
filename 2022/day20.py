#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/20

--- Day 20: Grove Positioning System ---

It's finally time to meet back up with the Elves. When you try to contact them,
however, you get no reply. Perhaps you're out of range?

You know they're headed to the grove where the star fruit grows, so if you can
figure out where that is, you should be able to meet back up with them.

Fortunately, your handheld device has a file (your puzzle input) that contains
the grove's coordinates! Unfortunately, the file is encrypted - just in case
the device were to fall into the wrong hands.

Maybe you can decrypt it?

When you were still back at the camp, you overheard some Elves talking about
coordinate file encryption. The main operation involved in decrypting the file
is called mixing.

The encrypted file is a list of numbers. To mix the file, move each number
forward or backward in the file a number of positions equal to the value of the
number being moved. The list is circular, so moving a number off one end of the
list wraps back around to the other end as if the ends were connected.

For example, to move the 1 in a sequence like 4, 5, 6, 1, 7, 8, 9, the 1 moves
one position forward: 4, 5, 6, 7, 1, 8, 9. To move the -2 in a sequence like 4,
-2, 5, 6, 7, 8, 9, the -2 moves two positions backward, wrapping around: 4, 5,
6, 7, 8, -2, 9.

The numbers should be moved in the order they originally appear in the
encrypted file. Numbers moving around during the mixing process do not change
the order in which the numbers are moved.

Consider this encrypted file:

1
2
-3
3
-2
0
4

Mixing this file proceeds as follows:

Initial arrangement:
1, 2, -3, 3, -2, 0, 4

1 moves between 2 and -3:
2, 1, -3, 3, -2, 0, 4

2 moves between -3 and 3:
1, -3, 2, 3, -2, 0, 4

-3 moves between -2 and 0:
1, 2, 3, -2, -3, 0, 4

3 moves between 0 and 4:
1, 2, -2, -3, 0, 3, 4

-2 moves between 4 and 1:
1, 2, -3, 0, 3, 4, -2

0 does not move:
1, 2, -3, 0, 3, 4, -2

4 moves between -3 and 0:
1, 2, -3, 4, 0, 3, -2

Then, the grove coordinates can be found by looking at the 1000th, 2000th, and
3000th numbers after the value 0, wrapping around the list as necessary. In the
above example, the 1000th number after 0 is 4, the 2000th is -3, and the 3000th
is 2; adding these together produces 3.

Mix your encrypted file exactly once. What is the sum of the three numbers that
form the grove coordinates?

--- Part Two ---

The grove coordinate values seem nonsensical. While you ponder the mysteries of
Elf encryption, you suddenly remember the rest of the decryption routine you
overheard back at camp.

First, you need to apply the decryption key, 811589153. Multiply each number by
the decryption key before you begin; this will produce the actual list of
numbers to mix.

Second, you need to mix the list of numbers ten times. The order in which the
numbers are mixed does not change during mixing; the numbers are still moved in
the order they appeared in the original, pre-mixed list. (So, if -3 appears
fourth in the original list of numbers to mix, -3 will be the fourth number to
move during each round of mixing.)

Using the same example as above:

Initial arrangement:
811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612

After 1 round of mixing:
0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153

After 2 rounds of mixing:
0, 2434767459, 1623178306, 3246356612, -2434767459, -1623178306, 811589153

After 3 rounds of mixing:
0, 811589153, 2434767459, 3246356612, 1623178306, -1623178306, -2434767459

After 4 rounds of mixing:
0, 1623178306, -2434767459, 811589153, 2434767459, 3246356612, -1623178306

After 5 rounds of mixing:
0, 811589153, -1623178306, 1623178306, -2434767459, 3246356612, 2434767459

After 6 rounds of mixing:
0, 811589153, -1623178306, 3246356612, -2434767459, 1623178306, 2434767459

After 7 rounds of mixing:
0, -2434767459, 2434767459, 1623178306, -1623178306, 811589153, 3246356612

After 8 rounds of mixing:
0, 1623178306, 3246356612, 811589153, -2434767459, 2434767459, -1623178306

After 9 rounds of mixing:
0, 811589153, 1623178306, -2434767459, 3246356612, 2434767459, -1623178306

After 10 rounds of mixing:
0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153

The grove coordinates can still be found in the same way. Here, the 1000th
number after 0 is 811589153, the 2000th is 2434767459, and the 3000th is
-1623178306; adding these together produces 1623178306.

Apply the decryption key and mix your encrypted file ten times. What is the sum
of the three numbers that form the grove coordinates?
'''
import collections
from typing import TextIO

# Local imports
from aoc2022 import AOC2022

DEFAULT_KEY = 1


class Cipher:
    '''
    Implements the Grove Positioning System
    '''
    def __init__(
        self,
        fh: TextIO,
        key: int = DEFAULT_KEY,
    ) -> None:
        '''
        Load the cipher data from the filehandle
        '''
        self.data = collections.deque(
            enumerate(map(lambda x: int(x) * key, fh))
        )

    @property
    def coordinates(self) -> int:
        '''
        Calculate the coordinates by first finding the index of the zero value,
        and then adding together the values at offset 1000, 2000, and 3000 from
        that position
        '''
        # Find the queue index of the zero value
        pointer = enumerate(self.data)
        while (item := next(pointer))[1][1] != 0:
            pass
        index = item[0]

        return sum(
            self.data[(index + offset) % len(self.data)][1]
            for offset in (1000, 2000, 3000)
        )

    def decrypt(self, rounds: int = 1) -> None:
        '''
        Perform decryption logic
        '''
        original_order = list(self.data)
        for _ in range(rounds):
            for item in original_order:
                # Rotate until we get to the location of this value
                self.data.rotate(-self.data.index(item))
                # Pop the value off the list, and then rotate again by that
                # amount to point the front of the queue at the location where
                # we need to move it
                self.data.rotate(-self.data.popleft()[1])
                # Place the the value in its new location
                self.data.appendleft(item)


class AOC2022Day20(AOC2022):
    '''
    Day 20 of Advent of Code 2022
    '''
    day = 20

    def load_cipher(self, key=DEFAULT_KEY) -> Cipher:
        '''
        Load the input file into a Cipher object
        '''
        with self.input.open() as fh:
            return Cipher(fh, key=key)

    def part1(self) -> int:
        '''
        Decrypt the cipher and return the coordinates
        '''
        cipher = self.load_cipher()
        cipher.decrypt()
        return cipher.coordinates

    def part2(self) -> int:
        '''
        Decrypt the cipher (10 rounds) using the key from part 2
        '''
        cipher = self.load_cipher(key=811589153)
        cipher.decrypt(rounds=10)
        return cipher.coordinates


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day20(example=True)
    aoc.validate(aoc.part1(), 3)
    aoc.validate(aoc.part2(), 1623178306)
    # Run against actual data
    aoc = AOC2022Day20(example=False)
    aoc.run()
