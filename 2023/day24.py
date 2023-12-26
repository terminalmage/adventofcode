#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/24
'''
import itertools
import re

# 3rd-party imports
import z3

# Local imports
from aoc import AOC, Coordinate, LineSegment


class AOC2023Day24(AOC):
    '''
    Day 24 of Advent of Code 2023
    '''
    day = 24

    int_re = re.compile(r'-?\d+')

    def part1(self) -> int:
        '''
        Calculate number of intersections that happen within the test area
        '''
        if self.example:
            min_x = min_y = 7
            max_x = max_y = 27
        else:
            min_x = min_y = 200000000000000
            max_x = max_y = 400000000000000

        paths: tuple[LineSegment] = tuple(
            LineSegment(
                Coordinate(x1, y1),
                Coordinate(x1 + x2, y1 + y2),
            )
            for x1, y1, _, x2, y2, _ in (
                tuple(int(x) for x in self.int_re.findall(line))
                for line in self.input.read_text().splitlines()
            )
        )

        intersections: dict[frozenset[LineSegment], Coordinate] = {}
        for seg1, seg2 in itertools.combinations(paths, 2):
            intersect = seg1 & seg2
            if intersect is not None:
                # Rule out past intersections
                vx1 = seg1.second.x - seg1.first.x
                vx2 = seg2.second.x - seg2.first.x
                # pylint: disable=too-many-boolean-expressions
                if (
                    intersect.x > seg1.first.x and vx1 > 0
                    or intersect.x < seg1.first.x and vx1 < 0
                ) and (
                    intersect.x > seg2.first.x and vx2 > 0
                    or intersect.x < seg2.first.x and vx2 < 0
                ):
                    intersections[frozenset({seg1, seg2})] = intersect
                # pylint: enable=too-many-boolean-expressions

        return sum(
            min_x <= inter.x <= max_x
            and min_y <= inter.y <= max_y
            for inter in intersections.values() if inter is not None
        )

    def part2(self) -> int:
        '''
        Use z3 to cheat and get the answer to this awful puzzle
        '''
        lines: list[str] = self.input.read_text().splitlines()
        # Reduce the number of hailstones down to a smaller subset, with the
        # assumption that rock that collides with 10% of them will be the
        # solution to this puzzle.
        params: tuple[tuple[int]] = tuple(
            tuple(int(x) for x in self.int_re.findall(line))
            for line in lines[:len(lines) // 10]
        )

        x, y, z = z3.BitVecs('x y z', 51)
        vx, vy, vz = z3.BitVecs('vx vy vz', 51)
        times: list[z3.BitVec] = []

        solver: z3.Solver = z3.Solver()
        for index, hailstone in enumerate(params):
            h_pos_x, h_pos_y, h_pos_z, h_vel_x, h_vel_y, h_vel_z = hailstone
            h_time: z3.BitVec = z3.BitVec(f'hailstone{index}_t', 51)
            # The time for collision must be in the future
            solver.add(h_time > 0)
            # The x, y, and z positions for each hailstone at time h_time for
            # the solution must match that of each hailstone
            solver.add(x + (vx * h_time) == h_pos_x + (h_vel_x * h_time))
            solver.add(y + (vy * h_time) == h_pos_y + (h_vel_y * h_time))
            solver.add(z + (vz * h_time) == h_pos_z + (h_vel_z * h_time))
            times.append(h_time)

        solver.add(z3.Distinct(times))

        if solver.check() != z3.sat:
            raise ValueError('No solution')

        return sum(
            solver.model()[pos].as_long()
            for pos in (x, y, z)
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2023Day24(example=True)
    aoc.validate(aoc.part1(), 2)
    # Run against actual data
    aoc = AOC2023Day24(example=False)
    aoc.run()
