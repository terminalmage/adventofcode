#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/4
'''
import collections
import itertools
import re
import string
import textwrap
from collections.abc import Generator

# Local imports
from aoc import AOC

# Typing shortcuts
RoomData = tuple[str, int, str]


class AOC2016Day4(AOC):
    '''
    Day 4 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        aaaaa-bbb-z-y-x-123[abxyz]
        a-b-c-d-e-f-g-h-987[abcde]
        not-a-real-room-404[oarel]
        totally-real-room-200[decoy]
        '''
    )

    validate_part1: int = 1514

    @property
    def room_data(self) -> Generator[RoomData, None, None]:
        '''
        Generator to produce a sequence of room data parsed from the input
        file. A regex is used to ensure
        '''
        room_re = re.compile(r'^([a-z-]+)-(\d+)\[([a-z]+)\]')
        for line in self.input.splitlines():
            m = room_re.match(line)
            if m:
                yield (m[1], int(m[2]), m[3])

    @property
    def real_rooms(self) -> Generator[RoomData, None, None]:
        '''
        Generator which only yields "real" rooms (those for which the checksum
        is correct)
        '''
        for room_data in self.room_data:
            if self.checksum(room_data[0]) == room_data[2]:
                yield room_data

    @staticmethod
    def checksum(name: str) -> str:
        '''
        Return the checksum for the specified room name
        '''
        return ''.join(
            letter for letter, freq in sorted(
                collections.Counter(name.replace('-', '')).items(),
                key=lambda kv: (-kv[1], kv[0]),
            )[:5]
        )

    @staticmethod
    def shift(name: str, sector_id: int) -> dict[int, str]:
        '''
        Implement the shift cipher by creating a translation table which shifts
        alphabetic characters by a position equal to the specified sector ID.
        '''
        # No need to shift hundreds of times, shifting will wrap every time
        # through the alphabet anyway.
        mod = sector_id % 26

        # Create translation table
        trans = str.maketrans(
            string.ascii_lowercase + '-',
            ''.join(
                itertools.islice(
                    itertools.cycle(string.ascii_lowercase),
                    mod,
                    mod + 26,
                )
            ) + ' '
        )

        # Return translated room name
        return name.translate(trans)

    def part1(self) -> int:
        '''
        Return the sum of sector IDs for real rooms
        '''
        return sum(sector_id for (_, sector_id, _) in self.real_rooms)

    def part2(self) -> int:
        '''
        Return the sector ID for northpole object storage
        '''
        # Generating checksums for each room to decide whether or not to apply
        # the shift cipher is slower than simply applying the cipher to every
        # room name.
        target: str = 'northpole object storage'
        for (name, sector_id, _) in self.room_data:
            if self.shift(name, sector_id) == target:
                return sector_id

        raise ValueError(f'Failed to find {target!r}')


if __name__ == '__main__':
    aoc = AOC2016Day4()
    aoc.run()
