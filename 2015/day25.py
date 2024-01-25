#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/25
'''
import re

# Local imports
from aoc import AOC


class AOC2015Day25(AOC):
    '''
    Day 25 of Advent of Code 2015
    '''
    # Values for modular exponentiation
    first = 20151125
    base = 252533
    mod = 33554393

    def post_init(self) -> None:
        '''
        Load the input data
        '''
        self.row: int
        self.col: int
        self.row, self.col = (int(n) for n in re.findall(r'\d+', self.input))

    def part1(self) -> int:
        '''
        To solve this puzzle, we need to get the nth item of a sequence. But we
        don't have n, all we have are a row and column number.

        Luckily, the we can calculate this position pretty easily because the
        sequence numbers proceed triangularly:

            https://en.wikipedia.org/wiki/Triangular_number

        From the puzzle description, here's the table showing code number
        progression:

               |   1   2   3   4   5   6
            ---+---+---+---+---+---+---+
             1 |   1   3   6  10  15  21
             2 |   2   5   9  14  20
             3 |   4   8  13  19
             4 |   7  12  18
             5 |  11  17
             6 |  16

        Given a row and column, we can imagine that point as being along the
        hypotenuse of a right isosceles triangle with non-hypotenuse sides of
        length (row + col - 1). Looking above, row 3, column 4 would be a point
        along the hypotenuse of a triangle with sides equal to 6 (that is, 3 +
        4 - 1).

        We can therefore calculate the 6th triangular number using the
        triangular number formula, with n replaced by 6:

            (n² + n) / 2

            (6² + 6) / 2
            (36 + 6) / 2
            42 / 2
            21

        This tells you that the top number in column 6 is 21. But we need
        column 4. Since the sequence increases by 1 per column, we just need to
        back up from column 6 to column 4 (a total decrease of the length of
        the triangle side minus the column we want, i.e. 6 - 4 or 2). This
        works out to 21 - 2, or 19. As you can see above, row 3 and column 4
        corresponds to number 19.

        Given all of the above, we can express a triangle number at row r and
        column c using the following equation:

            n = (((r + c - 1)² + (r + c)) / 2) - (r + c - 1 - c)

        In the last parenthetical, you'll notice that c cancels out. We can
        therefore simplify this slightly as:

            n = (((r + c - 1)² + (r + c)) / 2) - (r - 1)

        The code-generation algorithm for this is to take the previous code in
        the sequence, multiply it by 252533, then divide by 33554393 and take
        the remainder.

        We already have the first code number, so to get the code we need, we
        just need to start at the first item and repeat the algorithm n - 1
        times.

        Since we're multiplying by the same number each time through the
        algorithm and keeping the modulus, this algorthim is actually just
        modular exponentiation:

            https://en.wikipedia.org/wiki/Modular_exponentiation

        So instead of repeating the algorithm n-1 times, we can do this much
        faster using the pow() built-in from the Python standard library:

            https://docs.python.org/3/library/functions.html#pow
        '''
        side: int = self.row + self.col
        exp: int = (((side - 1)**2 + side) // 2) - (self.row - 1)
        return (pow(self.base, exp - 1, self.mod) * self.first) % self.mod


if __name__ == '__main__':
    aoc = AOC2015Day25()
    aoc.run()
