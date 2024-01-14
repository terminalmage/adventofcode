#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/23
'''
# Local imports
from aoc import AOC
from day12 import Computer, Program, Instruction


class SafeCracker(Computer):
    '''
    Modified Computer which implements "tgl" command
    '''
    def run(self, program: Program, **init: int) -> None:
        '''
        Run the program passed in
        '''
        # Apply any initial values passed in
        self.init(**init)

        # Index of where we are in the program's instruction set
        index: int = 0

        # Detect and optimize loops
        program: Program = self.optimize(program)

        while index < len(program):
            instruction: Instruction = program[index]

            match instruction.split():
                case ['tgl', register]:
                    new_index: int = index + int(getattr(self, register))
                    try:
                        target: Instruction = program[new_index]
                    except IndexError:
                        pass
                    else:
                        new_cmd: str
                        cmd: str
                        args: str
                        cmd, args = target.split(None, 1)
                        match cmd:
                            case 'inc':
                                new_cmd = 'dec'
                            case 'tgl':
                                new_cmd = 'inc'
                            case 'jnz':
                                new_cmd = 'cpy'
                            case 'cpy':
                                new_cmd = 'jnz'
                            case _:
                                raise ValueError(
                                    f'Unhandled toggle for {target!r}'
                                )
                        program[new_index] = f'{new_cmd} {args}'


                case _:
                    # The command wasn't a custom command. fall back to the
                    # parent class' instruction-handling logic to both process
                    # the instruction and get the index of the next instruction
                    # to run, and then skip to the next loop iteration.
                    index = self.exec(index, instruction)
                    continue

            # Custom argument handling was used, point the index at the
            # next instruction in the program.
            index += 1


class AOC2016Day23(AOC):
    '''
    Day 23 of Advent of Code 2016
    '''
    day = 23

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the computer and load the program from the puzzle input
        '''
        super().__init__(example=example)
        self.safe_cracker: SafeCracker = SafeCracker()
        self.program: Program = self.input.read_text().splitlines()

    def part1(self) -> int:
        '''
        Return the code generated by the safe cracker
        '''
        self.safe_cracker.run(self.program, a=0 if self.example else 7)
        return self.safe_cracker.a

    def part2(self) -> int:
        '''
        Return the code generated by the safe cracker with the value of
        register a initialized to 12
        '''
        self.safe_cracker.run(self.program, a=12)
        return self.safe_cracker.a


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day23(example=True)
    aoc.validate(aoc.part1(), 3)
    # Run against actual data
    aoc = AOC2016Day23(example=False)
    aoc.run()
