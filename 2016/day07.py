#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/7
'''
import re
import textwrap
from collections.abc import Iterator

# Local imports
from aoc import AOC


class AOC2016Day7(AOC):
    '''
    Day 7 of Advent of Code 2016
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        abba[mnop]qrst
        abcd[bddb]xyyx
        aaaa[qwer]tyui
        ioxxoj[asdfgh]zxcvbn
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        aba[bab]xyz
        xyx[xyx]xyx
        aaa[kek]eke
        zazbz[bzb]cdb
        '''
    )

    validate_part1: int = 2
    validate_part2: int = 3

    def ipv7(self, data: str) -> Iterator[str]:
        '''
        Generator which yields one IPv7 address at a time from the input file
        '''
        yield from data.splitlines()

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
    def aba_iter(section: str) -> Iterator[str]:
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
        splits: list[str] = self.split_ipv7(addr)
        if len(splits) == 1:
            # There were no brackets in the address, so it cannot possibly
            # support SSL
            return False

        supernet: list[str]
        for supernet in splits[::2]:
            aba: str
            for aba in self.aba_iter(supernet):
                # Invert the ABA sequence and check for it in each of the
                # hypernet sequences
                bab: str = aba.translate(str.maketrans(aba[:2], aba[1::-1]))
                if any(bab in hypernet for hypernet in splits[1::2]):
                    return True

        return False

    def part1(self) -> int:
        '''
        Return the password using the method from Part 1
        '''
        return sum(
            self.supports_tls(addr) for addr in self.ipv7(self.input_part1)
        )

    def part2(self) -> int:
        '''
        Return the password using the method from Part 2
        '''
        return sum(
            self.supports_ssl(addr) for addr in self.ipv7(self.input_part2)
        )


if __name__ == '__main__':
    aoc = AOC2016Day7()
    aoc.run()
