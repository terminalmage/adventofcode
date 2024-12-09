#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/9
'''
import itertools
import textwrap
from collections.abc import Iterator
from typing import Literal

# Local imports
from aoc import AOC


class AOC2024Day9(AOC):
    '''
    Day 9 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        2333133121414131402
        '''
    )

    validate_part1: int = 1928
    validate_part2: int = 2858

    def part1(self) -> int:
        '''
        Implement the "fragmenting algorithm" from Part 1 and return the
        checksum of the resulting disk arrangement.
        '''
        # Convert the puzzle input into a sequence of single-digit integers
        digits: Iterator[int] = map(int, self.input)

        # The disk is represented as a list of file IDs and empty strings.
        # The index of the list is the position, and the values represent the
        # contents of what occupies that position (either a file ID, or an
        # empty string if this position is empty.
        disk: list[str] = []
        free_space: int = 0
        try:
            file_id: int
            for file_id in itertools.count():
                # Add file to disk by adding N instances of the file ID
                disk.extend([file_id] * next(digits))
                # Add free space
                empty: int = next(digits)
                disk.extend([""] * empty)
                # Track free space here for later calculation
                free_space += empty
        except StopIteration:
            pass

        # Get a sequence of the indexes of each empty slot. We can iterate over
        # this to get the locations where fragments of files can be moved.
        empty_slots: Iterator[int] = iter(
            [x for x, y in enumerate(disk) if y == '']
        )

        # The process of filling in the gaps involves popping the rightmost
        # element of the list off, one at a time. If what was popped is a file
        # ID, then it is "moved" by putting its value back into the "disks"
        # list at the next empty slot (or discarding it if it contains an empty
        # string). Once the size of the "disks" list has reached the target
        # size, there is nothing left to move.
        target_size: int = len(disk) - free_space
        while len(disk) > target_size:
            file_id: int | Literal[''] = disk.pop(-1)
            if file_id != '':
                disk[next(empty_slots)] = file_id

        # Calculate and return checksum. The portion of the checksum for each
        # index in the list is that index times the file ID.
        return sum(x * y for x, y in enumerate(disk))

    def part2(self) -> int:
        '''
        Move whole files leftward if there is a large enough gap available.
        Once this process is completed, calculate and return the checksum.
        '''
        # Convert the puzzle input into a sequence of single-digit integers
        digits: Iterator[int] = map(int, self.input)

        # We don't need to track individual positions, since we will only be
        # moving whole files. Therefore, files can be represented by mapping a
        # file's ID to a tuple containing the start of the file and the file's
        # length. Gaps can be represented as a sequence of the same kind of
        # tuple (beginning of the gap, followed by size).
        files: dict[int, tuple[int, int]] = {}
        gaps: list[tuple[int, int]] = []
        # Position pointer, used to track the beginning of each file/gap
        ptr: int = 0
        try:
            file_id: int
            for file_id in itertools.count():
                # Add file to disk
                file_size: int = next(digits)
                files[file_id] = (ptr, file_size)
                ptr += file_size
                # Add free space
                free_size: int = next(digits)
                if free_size:
                    gaps.append((ptr, free_size))
                    ptr += free_size
        except StopIteration:
            pass

        # Try to move files leftward in reverse ID order
        for file_id in sorted(files, reverse=True):
            # Get the location where the file begins, as well as the size of
            # the file.
            file_start: int
            file_len: int
            file_start, file_len = files[file_id]

            # Iterate over the gaps until we find one large enough to
            # accommodate the file we're trying to move.
            gap_index: int
            gap_start: int
            gap_len: int
            for gap_index, (gap_start, gap_len) in enumerate(gaps):
                if gap_start > file_start:
                    # This gap is to the right of the current file. Since
                    # we're only moving files leftward, we can stop here.
                    break
                if gap_len < file_len:
                    # Can't move a file here, the gap is too small
                    continue
                # This gap will fit the file. "Move" it by updating its
                # location in the "files" dict, setting the start of the file
                # to the start of the gap.
                files[file_id] = (gap_start, file_len)
                # Calculate the new size of this gap by removing the size of
                # the file we just moved from it.
                new_gap_len: int = gap_len - file_len
                if not new_gap_len:
                    # This is no longer a gap, it's been entirely filled.
                    # Remove it from our list of gaps.
                    gaps.pop(gap_index)
                else:
                    # Update the gap to reflect the new start and length
                    gaps[gap_index] = (gap_start + file_len, new_gap_len)

                # We've moved the file, break out of inner loop so we can try
                # moving the next file
                break

        # For each position occupied by a file, its portion of the checksum
        # will be the product of that position and the file ID. What we have in
        # the "files" dict right now is a mapping of file IDs to tuples
        # containing the starting position and the length. Therefore, if we
        # iterate over the contents of this dict, we can calculate the portion
        # of the checksum for a given file, and then add those subtotals
        # together to get the full checksum.
        return sum(
            sum(
                map(
                    lambda pos, file_id=file_id: pos * file_id,
                    range(file_start, file_start + file_len)
                )
            )
            for file_id, (file_start, file_len) in files.items()
        )


if __name__ == '__main__':
    aoc = AOC2024Day9()
    aoc.run()
