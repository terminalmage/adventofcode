#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/23
'''
from __future__ import annotations
from collections import defaultdict

# Local imports
from aoc import AOC, MathMixin
from day18 import TabletBase

# Type hints
Instruction = str
Program = list[Instruction]


class Coprocessor(TabletBase):
    '''
    Implement the tablet from Part 1
    '''
    def __init__(self, program: Program) -> None:
        '''
        Set the initial state of the computer
        '''
        super().__init__(program)
        # Will be set whenever .reset() is run
        self.registers = self.counts = None
        self.reset()

    def reset(self) -> None:
        '''
        Reset all registers and counts
        '''
        self.registers: dict[str, int] = {r: 0 for r in 'abcdefgh'}
        self.counts: defaultdict[str, int] = defaultdict(int)

    def exec(self) -> None:
        '''
        Execute the specified instruction. If the instruction is not one with
        logic unique to Part 1, fall back to the parent class where logic
        shared by both puzzles is defined.
        '''
        # Number of instructions we should advance after executing this
        # instruction. Will be 1 unless a "jgz" is triggered.
        jump: int = 1

        instruction: Instruction = self.program[self.index]
        command: list[str] = instruction.split()
        self.counts[command[0]] += 1

        match command:
            case ['set', register, value]:
                self.registers[register]: int = self.resolve(value)

            case ['sub', register, value]:
                # Add the value (int or register) to the specified register
                self.registers[register] -= self.resolve(value)

            case ['mul', register, value]:
                # Multiple register by specified value (int or register),
                # updating the value in the specified register.
                self.registers[register] *= self.resolve(value)

            case ['jnz', register, value]:
                # Jump by the value in value, but only if the value in the
                # register is not zero.
                if self.resolve(register):
                    jump = self.resolve(value)

            case _:
                raise ValueError(f'Invalid instruction: {instruction!r}')

        # Return the index of the next instruction that should be executed
        self.index += jump

    def run_program(self) -> int:
        '''
        Run the program an instruction at a time until the Recover signal is
        processed on a register containing a nonzero value (which will raise a
        Recover exception containing the most-recently-emitted frequency.
        Return that frequency value.
        '''
        while self.index < len(self.program):
            self.exec()


class AOC2017Day23(AOC, MathMixin):
    '''
    Day 23 of Advent of Code 2017
    '''
    def part1(self) -> int:
        '''
        Return the number of times the program executes a 'mul' instruction, if
        all registers start with a value of 0.
        '''
        cp: Coprocessor = Coprocessor(self.input.splitlines())
        cp.run_program()
        return cp.counts['mul']

    def part2(self) -> int:
        '''
        Return the value stored in register h at the conclusion of this
        program, given that register a is initialized with a value of 1.

        Time for some code analysis!

        set b 81 <----------
        set c b             |
        jnz a 2             |   This first block of code does not loop (yay!).
        jnz 1 5             |   Since a=1, the "jnz 1 5" is jumped over. The
        mul b 100           |   result is that register b is set to 108100,
        sub b -100000       |   and register c is set to 17000 more (125100).
        set c b             |
        sub c -17000 <-------
        set f 1 <--------
        set d 2         |       There are three loops here. The outermost
        set e 2 <------ |       increments b by 17 at the end of the loop,
        set g d <---- | |       unless b == c. The two inner loops increment d
        mul g e     | | |       and e, respectively, each between 2 and the
        sub g b     | | |       current value of b. Within the inner loop, if
        jnz g 2     | | |       d * e == b, register f is set to 0. After the
        set f 0     | | |       two loops run to completion, if f == 0 then h
        sub e -1    | | |       is incremented by 1. f will only be 0 if at
        set g e     | | |       least 1 combination of d * e == b, which means
        sub g b     | | |       that what we're really doing here is counting
        jnz g -8 ---- | |       the non-primes between 108100 and 125100,
        sub d -1      | |       inclusive, while stepping 17 at a time.
        set g d       | |       However, since there's no break statement, we'd
        sub g b       | |       still end up testing trillions of combinations
        jnz g -13 ----- |       of d and e, no matter how quickly we discover
        jnz f 2         |       that a given value of b is non-prime.
        sub h -1        |
        set g b         |       I'm not even going to try to optimize the
        sub g c         |       instruction set here. Writing loop detection
        jnz g 2         |       for this is less appealing than oral surgery
        jnz 1 3         |       without anesthesia. Instead, I will simply
        sub b -17       |       implement the logic described above in Python.
        jnz 1 -23 <------
        '''
        b: int = 108_100
        c: int = b + 17_000
        return sum(not self.prime(d) for d in range(b, c + 1, 17))


if __name__ == '__main__':
    aoc = AOC2017Day23()
    aoc.run()
