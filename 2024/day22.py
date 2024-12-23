#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/22
'''
import textwrap
from collections import defaultdict

# Local imports
from aoc import AOC


class AOC2024Day22(AOC):
    '''
    Day 22 of Advent of Code 2024
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        1
        10
        100
        2024
        '''
    )
    example_data_part2: str = textwrap.dedent(
        '''
        1
        2
        3
        2024
        '''
    )

    validate_part1: int = 37327623
    validate_part2: int = 23

    @staticmethod
    def evolve(secret_number: int):
        '''
        Perform a series of operations, per the puzzle input. All the
        multiplications/divisions are powers of 2, and can thus be represented by
        bit shifting. For the modulo arithmetic, 16777216 is 2^24, or FFFFFF in
        hex. Therefore, N mod 16777216 is equal to N AND 0xFFFFFF.
        '''
        # Multiply by 64 (shift left 6 bits) and XOR
        secret_number ^= secret_number << 6
        secret_number &= 0xFFFFFF
        # Divide by 32 (shift right 5 bits) and XOR
        secret_number ^= secret_number >> 5
        secret_number &= 0xFFFFFF
        # Multiply by 2048 (shift left 11 bits) and XOR
        secret_number ^= secret_number << 11
        return secret_number & 0xFFFFFF

    def part1(self) -> int:
        '''
        Return the sum of all secrets after 2000 evolutions
        '''
        secrets: list[int] = list(map(int, self.input_part1.splitlines()))
        for _ in range(2000):
            i: int
            prev: int
            for i, prev in enumerate(secrets):
                secrets[i] = self.evolve(prev)
        return sum(secrets)

    def part2(self) -> int:
        '''
        Perform the same series of evolutions as in Part 1. For each initial
        secret, track the delta of the price (i.e. the ones position of the
        secret) for the previous 4 evolutions. The first time that a given
        sequence of deltas appears for a given secret, track the current price
        in a dictionary.

        At the end of 2000 evolutions, return the maximum sum of prices.
        '''
        secrets: list[int] = list(map(int, self.input_part2.splitlines()))
        last_4_changes: list[list[int]] = [[] for _ in secrets]

        ChangeKey = tuple[int, int, int, int]
        Changes = defaultdict[ChangeKey, list[int | None]]
        changes: Changes = defaultdict(lambda: [None for _ in secrets])

        for _ in range(2000):
            i: int
            prev: int
            for i, prev in enumerate(secrets):
                # Evolve the secret
                secrets[i] = self.evolve(prev)
                # The the price from the new secret
                new_price: int = secrets[i] % 10
                # Add the price delta to this secret's changes, and truncate
                # the list so that it only includes the previous 4.
                last_4_changes[i].append(new_price - prev % 10)
                last_4_changes[i] = last_4_changes[i][-4:]
                # Only track prices if we have a sequence of 4 deltas
                if len(last_4_changes[i]) < 4:
                    continue
                # Add this price to our changes dict if this is the first time
                # this secret has seen this sequence of deltas
                change_key: ChangeKey = tuple(last_4_changes[i])
                if changes[change_key][i] is None:
                    changes[change_key][i] = new_price

        # The values in the changes dict (i.e. buckets) will be lists of None
        # or int values. None if the corresponding sequence never appeared for
        # that secret, otherwise the price when that sequence first appears. To
        # get the best overall price, sum up the values in each bucket,
        # substituting 0 for each None. The largest of these sums is the best
        # overall price.
        return max(sum(i or 0 for i in bucket) for bucket in changes.values())


if __name__ == '__main__':
    aoc = AOC2024Day22()
    aoc.run()
