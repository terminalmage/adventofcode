#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/7
'''
import re
from collections.abc import Generator

# Local imports
from aoc import AOC


class AOC2016Day7(AOC):
    '''
    Day 7 of Advent of Code 2016
    '''
    day = 7

    def ipv7(self, part: int) -> Generator[str, None, None]:
        '''
        Generator which yields one IPv7 address at a time from the input file
        '''
        with self.get_input(part=part).open() as fh:
            for line in fh:
                yield line.rstrip()

    @staticmethod
    def split_ipv7(addr: str) -> list[str]:
        '''
        Split an IPv7 address into a list of alternating sections inside and
        outside of square brackets. Even-numbered list indexes will be outside
        of bracketed sections, while odd-numbered indexes will be inside of
        bracketed sections.
        '''
        return re.split(r'[\[\]]', addr)

    @staticmethod
    def has_abba(section: str) -> bool:
        '''
        Check to see the specified IPv7 address section contains an ABBA
        '''
        for i in range(len(section) - 3):
            # From the current string index, check the next 4 characters, in
            # 2-character groups. If the reverse of characters 3 and 4 is the
            # same string as the first two characters, and the first two
            # characters are not the same, then this is an ABBA.
            if (
                section[i:i+2] == section[i+3:i+1:-1]
                and section[i] != section[i+1]
            ):
                return True
        return False

    @staticmethod
    def aba_iter(section: str) -> Generator[str, None, None]:
        '''
        Generator which yields all ABA sequences in the specified section
        '''
        for i in range(len(section) - 2):
            # From the current string index, check the next 3 characters.
            # If the third character in that group is the same as the first,
            # and the second is not, then this is an ABA.
            if section[i] == section[i+2] and section[i] != section[i+1]:
                yield section[i:i+3]

    def supports_tls(self, addr: str) -> bool:
        '''
        Check to see if the IPv7 address supports TLS
        '''
        splits = self.split_ipv7(addr)
        if len(splits) == 1:
            # There were no brackets in the address, so it cannot possibly
            # support TLS
            return False

        return (
            not any(self.has_abba(section) for section in splits[1::2])
            and any(self.has_abba(section) for section in splits[::2])
        )

    def supports_ssl(self, addr: str) -> bool:
        '''
        Check to see if the IPv7 address supports SSL
        '''
        splits = self.split_ipv7(addr)
        if len(splits) == 1:
            # There were no brackets in the address, so it cannot possibly
            # support SSL
            return False

        for supernet in splits[::2]:
            for aba in self.aba_iter(supernet):
                # Invert the ABA sequence and check for it in each of the
                # hypernet sequences
                bab = aba.translate(str.maketrans(aba[:2], aba[1::-1]))
                if any(bab in hypernet for hypernet in splits[1::2]):
                    return True

        return False

    def part1(self) -> int:
        '''
        Return the password using the method from Part 1
        '''
        return sum(self.supports_tls(addr) for addr in self.ipv7(part=1))

    def part2(self) -> int:
        '''
        Return the password using the method from Part 1
        '''
        return sum(self.supports_ssl(addr) for addr in self.ipv7(part=2))


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day7(example=True)
    aoc.validate(aoc.part1(), 2)
    aoc.validate(aoc.part2(), 3)
    # Run against actual data
    aoc = AOC2016Day7(example=False)
    aoc.run()
