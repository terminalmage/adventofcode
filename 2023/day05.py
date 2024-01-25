#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/5
'''
import itertools
import re
import textwrap
from collections.abc import Generator
from dataclasses import dataclass

# Local imports
from aoc import AOC


@dataclass
class Range:
    '''
    Generic object defining a range of numbers
    '''
    begin: int
    length: int

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Range(begin={self.begin}, length={self.length})'

    def __contains__(self, value: int) -> bool:
        '''
        Enable membership check on Range instances
        '''
        return self.begin <= value < self.begin + self.length

    @property
    def end(self) -> int:
        '''
        Calculate and return the end of the range
        '''
        return self.begin + self.length

    def compare(self, other: 'Range') -> 'RangeSplit':
        '''
        Compare to another range, returning a RangeSplit detailing the
        intersection and before/after ranges
        '''
        overlap_begin = max(self.begin, other.begin)
        overlap_end = min(self.end, other.end)

        if overlap_end < overlap_begin:
            # Ranges do not overlap. Therefore, this entire range is either
            # before or after the other range.
            if self.begin < other.begin:
                # Since these ranges do not overlap, and this range begins
                # before the other range, this range is entirely before the
                # other range.
                return RangeSplit(self, None, None)

            # This range is entirely after the other range
            return RangeSplit(None, None, self)

        # If we haven't returned yet, then the two ranges do overlap
        overlap = Range(overlap_begin, overlap_end - overlap_begin)

        # Calculate the ranges that come before and after the overlap, if
        # applicable.
        before = after = None
        if overlap_begin > self.begin:
            before = Range(self.begin, overlap_begin - self.begin)
        if overlap_end < self.end:
            after = Range(overlap_end, self.end - overlap_end)

        return RangeSplit(before, overlap, after)


@dataclass
class RangeSplit:
    '''
    Result of the comparison of two ranges.
    '''
    before: Range | None = None
    overlap: Range | None = None
    after: Range | None = None

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return (
            f'RangeSplit(before={self.before}, overlap={self.overlap}, '
            f'after={self.after})'
        )


@dataclass
class MapRule:
    '''
    A single mapping rule
    '''
    dest_begin: int
    source_begin: int
    length: int

    @property
    def delta(self) -> int:
        '''
        Difference between the start of the dest and source ranges. Used when
        applying a MapRule to a range that overlaps, in order to derive the
        translated range.
        '''
        return self.dest_begin - self.source_begin

    @property
    def dest_range(self) -> Range:
        '''
        Return a Range object derived from the beginning of the dest and the
        length of the mapping relationship.
        '''
        return Range(self.dest_begin, self.length)

    @property
    def source_range(self) -> Range:
        '''
        Return a Range object derived from the beginning of the source and the
        length of the mapping relationship.
        '''
        return Range(self.source_begin, self.length)


@dataclass
class Map:
    '''
    Generic class for numeric translation
    '''
    rules: tuple[MapRule]

    def follow(self, source: int) -> int:
        '''
        Resolves a single source number to its destination, according to the
        rules defined for this Map.
        '''
        for rule in self.rules:
            if source in rule.source_range:
                return source + rule.delta

        # If source was not in any of the ranges, the destination is the same
        # as the source
        return source

    def follow_range(self, range_obj: Range) -> Generator[Range, None, None]:
        '''
        Process the Map's rules against a range of numbers, instead of a single
        numerical value. The result will be a sequence of Range objects
        representing the result of following the Map's rules.
        '''
        # Start with the specified range
        ranges = [range_obj]

        # For each rule, compare each range in the "ranges" list against the
        # rule's source range. Overlapping segments are ones that match the
        # rule's source range, and must be translated (by adding the rule's
        # delta). Non-overlapping segments are held to be checked against the
        # other rules (not sure if this is strictly necessary).
        for rule in self.rules:
            new_ranges = []
            for _range in ranges:
                # Compare range against source range from the mapping rule
                split: RangeSplit = _range.compare(rule.source_range)
                if split.overlap:
                    # This range overlaps with the mapping rule. Yield a
                    # translated range (i.e. apply the rule's delta to the
                    # beginning of the overlapping segment).
                    yield Range(
                        split.overlap.begin + rule.delta,
                        split.overlap.length,
                    )
                # Save the non-overlapping segments
                new_ranges.extend(r for r in (split.before, split.after) if r)

            # Update ranges for next loop iteration
            ranges = new_ranges

        # Yield all remaining non-overlapping segments
        for item in ranges:
            yield item


class AOC2023Day5(AOC):
    '''
    Day 5 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
        '''
    )

    validate_part1: int = 35
    validate_part2: int = 46

    def post_init(self) -> None:
        '''
        Read in map data
        '''
        self.seed_ids: tuple[int, ...] = tuple(
            int(item)
            for item in re.search(
                r'seeds: (\d.+)$',
                self.input.partition('\n')[0]
            ).group(1).split()
        )

        self.maps: list[Map] = []
        map_def: str
        for map_def in re.finditer(
            r'[a-z-]+ map:\n([\d \n]+)',
            self.input,
            flags=re.MULTILINE,
        ):
            ranges: str = map_def.group(1)
            self.maps.append(
                Map(
                    tuple(
                        MapRule(*(int(num) for num in line.split()))
                        for line in ranges.strip().splitlines()
                    )
                )
            )

    def location(self, seed: int) -> int:
        '''
        Return the location for a given seed
        '''
        ptr: int = seed
        _map: Map
        for _map in self.maps:
            ptr = _map.follow(ptr)
        return ptr

    def part1(self) -> int:
        '''
        Return the lowest seed location number
        '''
        return min(self.location(seed) for seed in self.seed_ids)

    def part2(self) -> int:
        '''
        Return the lowest seed location number, assuming that seed_ids are
        interpreted as pairs of Range specifiers
        '''
        seed_ranges: list[Range] = [
            Range(begin, length)
            for begin, length in zip(self.seed_ids[::2], self.seed_ids[1::2])
        ]

        # Apply each map to each seed range. The result will be a sequence
        # of mapped ranges (ranges which have passed through each map
        # sequentially). Since all of the resulting ranges now contain seed
        # locations, we know that the range with the lowest starting point is
        # the lowest location number.
        _map: Map
        for _map in self.maps:
            seed_ranges: list[Range] = list(
                itertools.chain.from_iterable(
                    _map.follow_range(_range) for _range in seed_ranges
                )
            )

        return min(_range.begin for _range in seed_ranges)


if __name__ == '__main__':
    aoc = AOC2023Day5()
    aoc.run()
