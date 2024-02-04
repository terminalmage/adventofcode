#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/15
'''
import math
import re
import textwrap

# Local imports
from aoc import AOC

# Typing shortcuts
Numbers = tuple[int, ...]


class AOC2016Day15(AOC):
    '''
    Day 15 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        Disc #1 has 5 positions; at time=0, it is at position 4.
        Disc #2 has 2 positions; at time=0, it is at position 1.
        '''
    )

    validate_part1: int = 5

    # Set by post_init
    modulos = None
    positions = None

    def post_init(self) -> None:
        '''
        Load the puzzle data
        '''
        # Zipping a zipped sequence produces parallel unzipped sequences.
        # Gathering a sequence of position-count / position-number pairs from
        # the result of our regex pattern matching gives us such a sequence, so
        # we can unpack them into parallel tuples by running zip on the
        # sequence of number/remainder pairs.
        pat: re.Pattern = re.compile(r'(\d+) positions; .+ position (\d+)')
        self.modulos: Numbers
        self.positions: Numbers
        self.modulos, self.positions = zip(
            *(
                (int(m) for m in pat.search(line).groups())
                for line in self.input.splitlines()
            )
        )

    @staticmethod
    def solve(modulos: Numbers, positions: Numbers) -> int:
        '''
        Get the drop time for a capsule to pass through each disc's slot when
        that disc is at its zeroth position, using the Chinese Remainder
        Theorem.

            https://en.wikipedia.org/wiki/Chinese_remainder_theorem

        This theorem operates on a system of congruences:

            https://mathworld.wolfram.com/Congruence.html

        An example congruence would be:

            x ≡ 3(mod 5)

        For this congruence, valid values for x would include 3, 8, 13, etc.
        Negative numbers are also valid (-2, -7, -12, etc.), but for the
        purpose of this puzzle we are not considering negative values.

        The modulos for each of the congruences in the series must be coprime
        with every other modulo (i.e. their greatest common denominator must be
        1).

        So, for the following three congruences, in the format x ≡ a(mod m):

            x ≡ 3(mod 5)    i.e. a₁(mod m₁)
            x ≡ 1(mod 7)    i.e. a₂(mod m₂)
            x ≡ 6(mod 8)    i.e. a₃(mod m₃)

        We can calculate a fourth congruence. Valid solutions to this fourth
        congruence will also be valid solutions for each of the other three
        congruences.

        The formula for this fourth congruence is:

            k              k
            Σ(aₙMₙMₙᵢ)(mod Π(mₙ))
           n=1            n=1

        For our series of three congruences, this works out to:

            (a₁M₁M₁ᵢ + a₂M₂M₂ᵢ + a₃M₃M₃ᵢ)(mod m₁m₂m₃)

        Mₙ is equal to the product of the modulos (i.e. m₁m₂m₃), divided by mₙ.

        Mₙᵢ is the inverse modulo of Mₙ mod mₙ, that is:

            MₙMₙᵢ = 1(mod mₙ)

        Which can be simplified as:

            Mₙᵢ = (1/Mₙ)(mod mₙ)    OR  Mₙᵢ = Mₙ⁻¹(mod mₙ)

        The inverse modulo can either be be calculated using the Extended
        Euclidian Algorithm, or failing that can be simply inferred by trying
        values. If aₙ is 0, then Mₙᵢ is also 0. Otherwise, you can start
        counting from 1 to mₙ-1, and substitute your guess for Mₙᵢ in the
        formula MₙMₙᵢ = 1(mod mₙ) until the two sides are equal.

        But ain't nobody got time for that. Python's pow() builtin does modular
        exponentiation easily (and far more efficiently than I would). The
        inverse modulo can be calculated using pow(Mₙ, -1, mₙ).

        Using the congruences above:

            M₁ = 280 / 5 = 56
            M₁ᵢ = 56⁻¹(mod 5) = 1
            M₂ = 280 / 7 = 40
            M₂ᵢ = 40⁻¹(mod 7) = 3
            M₃ = 280 / 8 = 35
            M₃ᵢ = 35⁻¹(mod 8) = 3

        Plugging this in to the formula, we get:

            ((3*56*1) + (1*40*3) + (6*35*3))(mod (5*7*8))
            (168 + 120 + 630)(mod 280)
            918(mod 280)

        Which is equivalent to (918 % 280)(mod 280), or:

            78(mod 280)

        Our aₙ here (78) can now be plugged into our other three congruences
        and be a valid x:

            78 ≡ 3(mod 5)
            78 ≡ 1(mod 7)
            78 ≡ 6(mod 8)

        78 / 5 is 15 with remainder 3.
        78 / 7 is 11 with remainder 1.
        78 / 8 is 9 with remainder 6.

        Looking at the input data, for each disc we get the number of
        positions, as well as the disc's position at t=0.

        As noted above, for the CRT to work, the modulos (i.e. the number of
        positions of each disc) must be coprime with that of each of the other
        discs. That is, the greatest common denominator of any one disc's
        positions and each other disc's positions must be 1. All of the
        position counts are unique primes, so each of them is guaranteed to be
        coprime with all of the other discs. The input is therefore suitable to
        use the CRT.

        We can think of the "remainders" as the number of seconds before a disc
        reaches position 0, and the number of positions for each disc as our
        modulos.

        But we have some work to do with the input data to get those remainder
        values. For each disc, the puzzle input gives us the number of
        positions and the position number (from 0 to n-1) at t=0. However, a
        capsule dropped at a given time (t) won't arrive at the first disc
        until t+1, the second disc until t+2, etc.

        Since we know what the positions are at t=0, let's imagine a capsule
        dropped at t=0. Our parallel tuples of values from the input are
        zero-indexed (i.e. disc 1 is at index 0, disc 2 at index 1, etc.), so
        the first disc (index 0) will shift 1 position before the capsule
        reaches it. The second disc (index 1) will shift 2 positions before the
        capsule reaches it, etc. This can be expressed as a given disc
        advancing index + 1 positions between the drop time and the time the
        capsule reaches that disc. So, if we add the index + 1 to the t=0
        position, we'll get the time-shifted position that disc would be in
        when a capsule dropped at t=0 reaches it. Positions only run from 0 to
        n-1 (where n is the number of positions), so we'll need to take the
        remainder again to get the actual position number with the time shift
        applied. So the time-shifted position for a disc would be equal to:

            (t=0 position + disc index + 1) % number of disc's positions

        With this time-shift applied to all of our t=0 positions, what we have
        now are _still_ not remainders, but time-shifted _positions_. To get
        the remainder value (the number of seconds before a given disc is back
        at position 0), we simply need to subtract our time-shifted position
        from the total number of positions for that disc.

        For example, assume that the 4th disc (index 3) has 5 positions and a
        t=0 position of 4. A capsule dropped at t=0 will reach this disc 4
        seconds later, putting it at position 3. This will leave it 2
        positions away (i.e. 5 - 3) from being back to position 0. This would
        be equivalent to the following congruence:

            x ≡ 2(mod 5)

        Subtracting the time-shifted position for each disc from that discs
        total number of positions will give us the remainder for the congruence
        represented by that disc (i.e. our aₙ values).
        '''
        # Apply time shifts to the positions, and calculate the remainder value
        # (i.e. aₙ) for each congruence, as described above.
        remainders: Numbers = tuple(
            modulos[i] - ((p + i + 1) % modulos[i])
            for i, p in enumerate(positions)
        )

        # Calculate the product of the modulos (i.e. m₁m₂...mₙ)
        prod: int = math.prod(modulos)

        # Calculate Mₙ for each disc (i.e. modulo product divided by the modulo)
        multipliers: Numbers = tuple(prod // m for m in modulos)

        # Calculate the inverse modulo (i.e. Mₙᵢ) for each disc
        inv_mods: Numbers = tuple(
            pow(multiplier, -1, modulo)
            for multiplier, modulo in zip(multipliers, modulos)
        )

        # Add up all the aₙMₙMₙᵢ products, divide by the product of the
        # modulos, and take the remainder. The result is our solution.
        return sum(
            remainders[i] * multipliers[i] * inv_mods[i]
            for i in range(len(modulos))
        ) % prod

    def part1(self) -> int:
        '''
        Solve for the discs defined in the input data.
        '''
        return self.solve(self.modulos, self.positions)

    def part2(self) -> int:
        '''
        Solve with the additional disc defined in Part 2 (11 positions, with
        t=0 position of 0).
        '''
        return self.solve(
            self.modulos + (11,),
            self.positions + (0,),
        )


if __name__ == '__main__':
    aoc = AOC2016Day15()
    aoc.run()
