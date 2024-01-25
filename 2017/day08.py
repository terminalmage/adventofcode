#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/8
'''
import operator
import re
import textwrap
from collections import defaultdict
from collections.abc import Callable

# Local imports
from aoc import AOC

Instruction = str
Program = tuple[Instruction]
Registers = defaultdict[str, int]


class AOC2017Day8(AOC):
    '''
    Day 8 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        b inc 5 if a > 1
        a inc 1 if b < 5
        c dec -10 if a >= 1
        c inc -20 if c == 10
        '''
    )

    validate_part1: int = 1
    validate_part2: int = 10

    def post_init(self) -> None:
        '''
        Load the program from the puzzle input
        '''
        program: Program = tuple(self.input.splitlines())
        registers: Registers = defaultdict(int)

        # Type hints
        instruction: Instruction
        CompFunc = Callable[[int, int], bool]
        MathFunc = Callable[[int, int], int]

        comp: dict[str, CompFunc] = {
            '<': operator.lt,
            '<=': operator.le,
            '>': operator.gt,
            '>=': operator.ge,
            '==': operator.eq,
            '!=': operator.ne,
        }
        inst_re: re.Pattern = re.compile(
            r'^(\w+) (inc|dec) (-?\d+) if (\w+) ([<>!=]+) (-?\d+)$'
        )

        self.max_during_run: int = 0
        for instruction in program:
            m: re.Match | None = inst_re.match(instruction)
            try:
                reg1: str = m.group(1)
                change: MathFunc = operator.add \
                    if m.group(2) == 'inc' \
                    else operator.sub
                delta: int = int(m.group(3))
                reg2: str = m.group(4)
                compfunc: CompFunc = comp[m.group(5)]
                rvalue: int = int(m.group(6))
            except AttributeError as exc:
                raise ValueError(
                    f'Failed to parse instruction: {instruction!r}'
                ) from exc
            except KeyError as exc:
                raise ValueError(f'Invalid operator: {m.group(5)!r}') from exc

            if compfunc(registers[reg2], rvalue):
                registers[reg1] = change(registers[reg1], delta)
                self.max_during_run = max(self.max_during_run, registers[reg1])

        self.max_after_run: int = max(registers.values())

    def part1(self) -> int:
        '''
        Return the max value in any register after program has finished
        '''
        return self.max_after_run

    def part2(self) -> int:
        '''
        Return the max value at any point during the program's run
        '''
        return self.max_during_run


if __name__ == '__main__':
    aoc = AOC2017Day8()
    aoc.run()
