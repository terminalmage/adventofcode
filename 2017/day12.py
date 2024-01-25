#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/12
'''
import re
import textwrap
from collections import defaultdict, deque

# Local imports
from aoc import AOC

# Type hints
ProgramID = int
ProgramGroup = frozenset[ProgramID]


class AOC2017Day12(AOC):
    '''
    Day 12 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        0 <-> 2
        1 <-> 1
        2 <-> 0, 3, 4
        3 <-> 2, 4
        4 <-> 2, 3, 6
        5 <-> 6
        6 <-> 4, 5
        '''
    )

    validate_part1: int = 6
    validate_part2: int = 2

    def post_init(self) -> None:
        '''
        Load the puzzle input
        '''
        self.programs: defaultdict[str, set] = defaultdict(set)
        for line in self.input.splitlines():
            ids: list[str] = [int(i) for i in re.findall(r'\d+', line)]
            program_id: str = ids[0]
            connected_id: str
            for connected_id in ids[1:]:
                self.programs[program_id].add(connected_id)
                self.programs[connected_id].add(program_id)

    def members(self, member: ProgramID) -> ProgramGroup:
        '''
        Returns a group of program IDs that make up the group containing the
        specified ID.
        '''
        group: set[ProgramID] = set()
        dq: deque[ProgramID] = deque([member])

        while dq:
            program_id: ProgramID = dq.popleft()

            # Skip already-added programs
            if program_id in group:
                continue

            # Add this program_id to the group
            group.add(program_id)

            # Add all of this program's connections to the queue
            dq.extend(self.programs[program_id])

        return frozenset(group)

    def part1(self) -> int:
        '''
        Return the number of the programs in the group that contains Program 0
        '''
        return len(self.members(0))

    def part2(self) -> int:
        '''
        Return the number of groups
        '''
        program_ids: set[ProgramID] = set(self.programs)
        groups: int = 0

        while program_ids:
            groups += 1
            program_ids -= self.members(next(iter(program_ids)))

        return groups


if __name__ == '__main__':
    aoc = AOC2017Day12()
    aoc.run()
