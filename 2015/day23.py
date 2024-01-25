#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/23
'''
from dataclasses import dataclass

# Local imports
from aoc import AOC

# Typing shortcuts
Command = str
Program = list[Command]


@dataclass
class Computer:
    '''
    Simulates a computer's registers and instructions
    '''
    a: int = 0
    b: int = 0

    def reset(self) -> None:
        '''
        Resets both registers to zero
        '''
        self.a = self.b = 0

    def exec(self, command: Command) -> int:
        '''
        Execute the specified command, returning the jump delta
        '''
        register_cmds = frozenset({'hlf', 'tpl', 'inc'})
        register_jump_cmds = frozenset({'jie', 'jio'})
        registers = 'ab'
        jump = 1

        match command.split():
            case [cmd, register] if (
                cmd in register_cmds
                and register in registers
            ):
                cur = getattr(self, register)
                match cmd:
                    case 'hlf':
                        new = cur // 2
                    case 'tpl':
                        new = cur * 3
                    case 'inc':
                        new = cur + 1
                    case _:
                        raise ValueError(
                            f'Missing definition for register command: '
                            f'{command}'
                        )
                setattr(self, register, new)
            case [cmd, register, offset] if (
                cmd in register_jump_cmds
                and register.rstrip(',') in registers
            ):
                register = register.rstrip(',')
                cur = getattr(self, register)
                match cmd:
                    case 'jie':
                        if getattr(self, register) % 2 == 0:
                            jump = int(offset)
                    case 'jio':
                        if getattr(self, register) == 1:
                            jump = int(offset)

            case ['jmp', offset]:
                jump = int(offset)

            case _:
                raise ValueError(f'Invalid command: {command}')

        return jump

    def run_program(self, program: Program) -> None:
        '''
        Run a series of commands until a jump condition jumps outside the
        bounds of the program.
        '''
        pos: int = 0
        while 0 <= pos < len(program):
            pos += self.exec(program[pos])


class AOC2015Day23(AOC):
    '''
    Day 23 of Advent of Code 2015
    '''
    def part1(self) -> int:
        '''
        Return the value of register b after running the program
        '''
        c = Computer()
        c.run_program(self.input.splitlines())
        return c.b

    def part2(self) -> int:
        '''
        Return the value of register b after running the program with the value
        of register a initialized to 1.
        '''
        c = Computer(a=1)
        c.run_program(self.input.splitlines())
        return c.b


if __name__ == '__main__':
    aoc = AOC2015Day23()
    aoc.run()
