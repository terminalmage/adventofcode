#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/18
'''
from __future__ import annotations
import textwrap
from collections import defaultdict, deque
from dataclasses import dataclass

# Local imports
from aoc import AOC

# Type hints
Instruction = str
Program = list[Instruction]


@dataclass
class Recover(Exception):
    '''
    Signaling exception to trigger end of program
    '''
    frequency: int


class TabletBase:
    '''
    Base functionality for both puzzles
    '''
    def __init__(self, program: Program) -> None:
        '''
        Set the initial state of the computer
        '''
        self.program: Program = program
        self.index: int | None = 0
        # This is included to prevent no-member lint failures. It must be set
        # to a proper defaultdict in a subclass' __init__.
        self.registers = None

    def resolve(self, value: str) -> int:
        '''
        Given a string, first attempt to return it as an integer value. If that
        fails, assume the value is the name of a register, and return the value
        stored in that register.
        '''
        try:
            return int(value)
        except ValueError:
            return self.registers[value]

    def exec(self) -> None:
        '''
        Execute the specified instruction, and advance the index the
        appropriate number of steps.
        '''
        # Number of instructions we should advance after executing this
        # instruction. Will be 1 unless a "jgz" is triggered.
        jump: int = 1

        instruction: Instruction = self.program[self.index]

        match instruction.split():
            case ['set', register, value]:
                self.registers[register]: int = self.resolve(value)

            case ['add', register, value]:
                # Add the value (int or register) to the specified register
                self.registers[register] += self.resolve(value)

            case ['mul', register, value]:
                # Multiple register by specified value (int or register),
                # updating the value in the specified register.
                self.registers[register] *= self.resolve(value)

            case ['mod', register, value]:
                # Divide register by specified value (int or register),
                # updating the value in the specified register with the
                # remainder of the division.
                self.registers[register] %= self.resolve(value)

            case ['snd', register]:
                raise NotImplementedError

            case ['rcv', register]:
                raise NotImplementedError

            case ['jgz', register, offset]:
                # Set the jump value to the specified offset, but only if the
                # value in the specified register is > 0.
                if self.resolve(register) > 0:
                    jump: int = int(self.resolve(offset))

            case _:
                raise ValueError(f'Invalid command: {instruction!r}')

        # Return the index of the next instruction that should be executed
        self.index += jump

    def run_program(self) -> int:
        '''
        Must be implemented in subclass
        '''
        raise NotImplementedError


class TabletPart1(TabletBase):
    '''
    Implement the tablet from Part 1
    '''
    def __init__(self, program: Program) -> None:
        '''
        Set the initial state of the computer
        '''
        super().__init__(program)
        self.registers: defaultdict[str, int] = defaultdict(int)
        self.frequency: int = 0

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

        match instruction.split():
            case ['snd', register]:
                self.frequency: int = self.resolve(register)

            case ['rcv', register]:
                # Trigger recovery if the specified register is != 0
                if self.resolve(register):
                    raise Recover(self.frequency)

            case _:
                # Fall back to base class for common instruction handling
                super().exec()
                return

        # Return the index of the next instruction that should be executed
        self.index += jump

    def run_program(self) -> int:
        '''
        Run the program an instruction at a time until the Recover signal is
        processed on a register containing a nonzero value (which will raise a
        Recover exception containing the most-recently-emitted frequency.
        Return that frequency value.
        '''
        try:
            while self.index < len(self.program):
                self.exec()
        except Recover as r:
            return r.frequency

        raise RuntimeError('Program ended without recovery')


class TabletPart2(TabletBase):
    '''
    Implement the tablet from Part 2
    '''
    def __init__(self, program: Program, program_id: int) -> None:
        '''
        Set the initial state of the tablet
        '''
        super().__init__(program)
        self.program_id: int = program_id
        self.registers: defaultdict[str, int] = defaultdict(lambda: self.program_id)
        self.queue: deque[int] = deque()
        self.waiting: bool = False
        self.sent: int = 0
        self.partner: TabletPart2 | None = None

    def set_partner(self, partner: TabletPart2) -> None:
        '''
        Set the Partner
        '''
        self.partner: TabletPart2 = partner

    @property
    def can_run(self) -> bool:
        '''
        Return True if the tablet is able to continue to run, otherwise False.
        If the program has ended without deadlock, the index will be None. If
        the program is in a waiting state, the program can only continue if the
        queue is not empty.
        '''
        return self.index is not None and (
            not self.waiting
            or (self.waiting and bool(self.queue))
        )

    def exec(self) -> None:
        '''
        Execute the specified instruction. If the instruction is not one with
        logic unique to Part 2, fall back to the parent class where logic
        shared by both puzzles is defined.
        '''
        jump: int = 1

        instruction: Instruction = self.program[self.index]

        match instruction.split():
            case ['snd', register]:
                self.partner.queue.append(self.resolve(register))
                self.sent += 1

            case ['rcv', register]:
                try:
                    self.registers[register] = self.queue.popleft()
                    self.waiting = False
                except IndexError:
                    self.waiting = True
                    return

            case _:
                # Fall back to base class for common instruction handling
                super().exec()
                return

        self.index += jump

    def run_program(self) -> None:
        '''
        Run the program an instruction at a time. After each instruction, check
        to see if the program is in a waiting state. If so, return so that the
        other program can run.

        If the end of the program is reached, set the index to None.
        '''
        if self.partner is None:
            raise ValueError('Partner not set!')

        if not self.can_run:
            return

        while self.index < len(self.program):
            self.exec()
            if self.waiting:
                return

        self.index = None


class AOC2017Day18(AOC):
    '''
    Day 18 of Advent of Code 2017
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        set a 1
        add a 2
        mul a a
        mod a 5
        snd a
        set a 0
        rcv a
        jgz a -1
        set a 1
        jgz a -2
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        snd 1
        snd 2
        snd p
        rcv a
        rcv b
        rcv c
        rcv d
        '''
    )

    validate_part1: int = 4
    validate_part2: int = 3

    def part1(self) -> int:
        '''
        Return the most recent frequency emitted by the Tablet when the Recover
        signal is processed on a register containing a nonzero value.
        '''
        tablet: TabletPart1 = TabletPart1(self.input_part1.splitlines())
        return tablet.run_program()

    def part2(self) -> int:
        '''
        Return the number of values emitted by tab1 once both programs are
        either deadlocked or completed.
        '''
        tab0 = TabletPart2(self.input_part2.splitlines(), program_id=0)
        tab1 = TabletPart2(self.input_part2.splitlines(), program_id=1)
        tab0.set_partner(tab1)
        tab1.set_partner(tab0)

        while tab0.can_run or tab1.can_run:
            tab0.run_program()
            tab1.run_program()

        return tab1.sent


if __name__ == '__main__':
    aoc = AOC2017Day18()
    aoc.run()
