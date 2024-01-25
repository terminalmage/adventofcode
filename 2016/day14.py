#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/14
'''
import functools
import hashlib
import itertools
import re
import textwrap

# Local imports
from aoc import AOC


DEFAULT_STRETCH: int = 0
TRIPLE: re.Pattern = re.compile(r'(\w)\1{2}')
FIVES: re.Pattern = re.compile(r'(\w)\1{4}')


@functools.cache
def get_hash(
    salt: str,
    index: int,
    stretch: int = DEFAULT_STRETCH
) -> str:
    '''
    Get the hash for the specified salt and index
    '''
    ret: str = hashlib.md5(f'{salt}{index}'.encode()).hexdigest()

    for _ in range(stretch):
        ret = hashlib.md5(ret.encode()).hexdigest()

    return ret


@functools.cache
def fives(
    salt: str,
    index: int,
    stretch: int = DEFAULT_STRETCH
) -> frozenset[str]:
    '''
    Returns a frozenset of the quintuples for the index'th hash
    '''
    return frozenset(
        itertools.chain.from_iterable(
            FIVES.findall(get_hash(salt, index, stretch))
        )
    )


class AOC2016Day14(AOC):
    '''
    Day 14 of Advent of Code 2016
    '''
    example_data: str = textwrap.dedent(
        '''
        abc
        '''
    )

    validate_part1: int = 22728
    validate_part2: int = 22551

    def key_index(self, key_id: int, stretch: int = DEFAULT_STRETCH) -> int:
        '''
        Find the index of the key_id'th key
        '''
        # Type hints
        index: int
        fives_index: int
        triple: re.Match | None

        key_ids: list[int] = []

        for index in itertools.count():
            triple = TRIPLE.search(get_hash(self.input, index, stretch))
            if triple:
                char: str = triple.group(1)
                for fives_index in range(index + 1, index + 1001):
                    if char in fives(self.input, fives_index, stretch):
                        key_ids.append(index)
                        if len(key_ids) == key_id:
                            return index
                        break

    def part1(self) -> int:
        '''
        Get the 64th key
        '''
        return self.key_index(64)

    def part2(self) -> int:
        '''
        Get the 64th key using a stretch factor of 2016
        '''
        return self.key_index(64, stretch=2016)


if __name__ == '__main__':
    aoc = AOC2016Day14()
    aoc.run()
