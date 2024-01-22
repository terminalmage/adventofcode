#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/5
'''
import hashlib
from collections import defaultdict
from collections.abc import Generator

# Local imports
from aoc import AOC

# Type hints
MD5 = str
MD5Record = tuple[MD5, int]


class AOC2016Day5(AOC):
    '''
    Day 5 of Advent of Code 2016
    '''
    def post_init(self) -> None:
        '''
        Load the door_id from the input and initialize the cache
        '''
        self.door_id = self.input.encode()
        self.cache: defaultdict[bytes, dict[int, MD5Record]] = defaultdict(dict)

    def hash_seq(
        self,
        length: int = 0,
    ) -> Generator[MD5, None, None]:
        '''
        Generator which returns a sequence of "interesting" hashes.

        If length is > 0, stop the sequence after that many hashes, otherwise
        produce hashes indefinitely.
        '''
        # Type hints
        md5: MD5
        idx: int
        found: int
        data: bytes

        idx = found = 0

        while True:
            # Return the next value in the sequence for this door_id, if we
            # have one in the cache.
            if found + 1 in self.cache[self.door_id]:
                (md5, idx) = self.cache[self.door_id][found + 1]
                yield md5
                found += 1
                idx += 1
                continue

            data = self.door_id + str(idx).encode()
            md5 = hashlib.md5(data).hexdigest()
            if md5.startswith('00000'):
                found += 1
                self.cache[self.door_id][found] = (md5, idx)
                yield md5
                if length > 0 and found == length:
                    break

            idx += 1

    def part1(self) -> str:
        '''
        Return the password using the method from Part 1
        '''
        return ''.join(md5[5] for md5 in self.hash_seq(8))

    def part2(self) -> str:
        '''
        Return the password using the method from Part 2
        '''
        length: int = 8
        cols: list[str | None] = length * [None]
        hashes: Generator[MD5, None, None] = self.hash_seq()
        while any(col is None for col in cols):
            pos: str
            char: str
            pos, char = next(hashes)[5:7]
            try:
                pos: int = int(pos)
            except ValueError:
                continue
            if pos >= length or cols[pos] is not None:
                continue
            cols[pos] = char

        return ''.join(cols)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day5(example=True)
    aoc.validate(aoc.part1(), '18f47a30')
    aoc.validate(aoc.part2(), '05ace8e3')
    # Run against actual data
    aoc = AOC2016Day5(example=False)
    aoc.run()
