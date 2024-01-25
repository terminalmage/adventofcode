#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/7
'''
import collections
import re
import textwrap
from dataclasses import dataclass, field
from typing import Self

# Local imports
from aoc import AOC


@dataclass
class Program:
    '''
    Hold information about a given program
    '''
    name: str
    weight: int
    parent: Self | None = None
    children: list[Self] = field(default_factory=list)

    @property
    def total_weight(self) -> int:
        '''
        Return the total weight (this program's weight plus the total weight of
        all its children).
        '''
        return self.weight + sum(child.total_weight for child in self.children)


class AOC2017Day7(AOC):
    '''
    Day 7 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        pbga (66)
        xhth (57)
        ebii (61)
        havc (66)
        ktlj (57)
        fwft (72) -> ktlj, cntj, xhth
        qoyq (66)
        padx (45) -> pbga, havc, qoyq
        tknk (41) -> ugml, padx, fwft
        jptl (61)
        ugml (68) -> gyxo, ebii, jptl
        gyxo (61)
        cntj (57)
        '''
    )

    validate_part1: str = 'tknk'
    validate_part2: int = 60

    def post_init(self) -> None:
        '''
        Initialize Program instances with their weights
        '''
        lines: list[str] = self.input.splitlines()
        # We will make a second pass over the input to link parents/children,
        # but first we need the Program instances to exist so they can be
        # linked properly.
        self.programs: dict[str, Program] = {
            m.group(1): Program(name=m.group(1), weight=int(m.group(2)))
            for m in (
                re.match(r'(\w+) \((\d+)\)', line)
                for line in lines
            ) if m
        }

        # Link parents/children
        for line in lines:
            program: str
            children: str
            try:
                program, children = re.match(r'(\w+).+ -> (.+)$', line).groups()
            except AttributeError:
                # No children for this program
                continue
            for child in (c.strip() for c in children.split(',')):
                self.programs[program].children.append(self.programs[child])
                self.programs[child].parent = self.programs[program]

        # Discover bottom program
        program: Program
        for program in self.programs.values():
            if program.parent is None:
                self.bottom: Program = program
                break
        else:
            raise ValueError('Failed to detect bottom program')

    def find_unbalanced(self, program: Program | None = None) -> int:
        '''
        Find the unbalanced program, and return the weight it would need to be
        changed to for the entire tower to be balanced.
        '''
        program = program or self.bottom

        # Get mapping of bottom program's children, to their total weights
        children: dict[str, int] = {
            p.name: p.total_weight for p in program.children
        }

        # Get count of weights to find the unbalanced weight value
        target: int
        other: int
        target, other = (
            c[0] for c in
            collections.Counter(children.values()).most_common()
        )

        # Find the program which has that unbalanced weight
        name: str
        weight: int
        for name, weight in children.items():
            if weight == other:
                unbalanced: Program = self.programs[name]
                break
        else:
            raise ValueError('Failed to detect unbalanced program')

        # If this program's children are perfectly balanced, we have found the
        # one unbalanced program. Return the ideal weight for this program.
        if len(set(c.total_weight for c in unbalanced.children)) == 1:
            return unbalanced.weight + target - other

        # The unbalanced program is further up the tower, keep recursing until
        # we find it.
        return self.find_unbalanced(unbalanced)

    def part1(self) -> str:
        '''
        Return the name of the bottom program
        '''
        return self.bottom.name

    def part2(self) -> int:
        '''
        Return the ideal weight for the one unbalanced program
        '''
        return self.find_unbalanced()


if __name__ == '__main__':
    aoc = AOC2017Day7()
    aoc.run()
