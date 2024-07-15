#!/usr/bin/env python
"""
https://adventofcode.com/2018/day/19
"""
import textwrap

# Local imports
from aoc import AOC, MathMixin
from day16 import opcode, Emulator, Input, Instruction, Output, Program, Register

# Type hints
Register = int
Registers = tuple[Register, Register, Register, Register, Register, Register] | list[Register]


class EmulatorV2(Emulator, MathMixin):
    """
    Modified emulator which supports an instruction pointer

    Observations:

        1. The first thing that happens is a skip forward.

        2. After the skip, a number is calculated and stored into register 4
           (r4), and then if register 0 (r0) is set to 0, execution jumps back
           near the top, where two nested loops are located (details below).

        2. If r0 is _not_ set to 1, then a _much_ larger number is calculated,
           and then it is added to register 4, updating that register. At this
           point, r0 is zeroed out and execution jumps back near the top, where
           two nested loops are located (details below).

        3. To implement an equality check, several instructions are used:
           a. A register is used to store the result of an arithmetic
              operation (e.g. instruction 3 below).
           b. The eqrr opcode is used to check if the result is equal to the
              value of another register.
           c. The result of the eqrr is to set a register to either 1 or 0.
              This is then fed into the instcution pointer register to skip
              around a line of code.
           d. This method is used twice in the inner loop. The 2nd instance is
              used to conditionally jump to to of the inner loop to repeat it,
              essentially turning this into a while loop.
           e. The same method is used to implement the outer loop.
           f. Lines 1-11 can therefore be expressed in Python like so:

                r5 = 1
                r2 = 1
                while r5 <= r4:
                  while r2 <= r4:    # r4 was calculated prior to entering loops
                    if (r5 * r2) == r4:
                      r0 += r5
                    r2 += 1
                  r5 += 1

            g. The above is an extremely inefficient way of setting register 0
               to the sum of all the factors of whatever value is stored in
               regsiter 4. Note that in the case of r0 == 1, r0 starts with 1,
               so

        4. The entire program can be reduced to returning the sum of the
           factors of whichever number is stored in r4. Therefore, the loop can
           be bypassed and replaced with a new opcode function which sets the
           output register to the sum of the factors of the first input
           (ignoring the 2nd input), and then exiting the program.

        5. Contents of the program with notes explaining instructions

                 #ip 3              (r3 is instruction pointer)
                 0  addi 3 16 3     Jumps to line 17 (JUMP1)
    (JUMP2)      1  seti 1 6 5      r5 = 1
    (LOOP 1)     2  seti 1 8 2      r2 = 1  <------------------------
    (LOOP 2)     3  mulr 5 2 1      r1 = r5 * r2  <--------------   |
                 4  eqrr 1 4 1      r1 = 1 if r1 == r4 else 0   |   |
                 5  addr 1 3 3      r3 += r1                    |   |  if (r5 * r2) == r4:
                 6  addi 3 1 3      r3 += 1                     |   |      r0 += r5
                 7  addr 5 0 0      r0 += r5                    |   |
                 8  addi 2 1 2      r2 += 1                     |   |
                 9  gtrr 2 4 1      r1 == 1 if r2 > r4 else 0   |   |
                10  addr 3 1 3      r3 += 1                     |   |
                11  seti 2 3 3      r3 = 2  ---------------------   |
                12  addi 5 1 5      r5 += 1                         |
                13  gtrr 5 4 1      r1 = 1 if r5 > r4 else 0        |
                14  addr 1 3 3      r3 += r1                        |
                15  seti 1 8 3      r3 = 1  -------------------------
                16  mulr 3 3 3      r3 *= 3 (multiplies instr ptr by 3, ending program)
    (JUMP1)     17  addi 4 2 4      r4 = 2
                18  mulr 4 4 4      r4 *= r4    r4 = 2 ** 2 = 4
                19  mulr 3 4 4      r4 *= 19    r4 = 4 * 19 = 76
                20  muli 4 11 4     r4 *= 11    r4 = 76 * 11 = 836
                21  addi 1 6 1      r1 = 6
                22  mulr 1 3 1      r1 *= 22    r1 = 6 * 22 = 132
                23  addi 1 10 1     r1 += 10    r1 = 132 + 10 = 142
                24  addr 4 1 4      r4 += r1    r4 = 836 + 142 = 968
                25  addr 3 0 3      Adds starting value of r0 to r3 (skips jump if r0 > 0)
                26  seti 0 0 3      Sets instruction pointer to 0 (jump to JUMP2)
                27  setr 3 9 1      r1 = r3     r1 = 27
                28  mulr 1 3 1      r1 *= r3    r1 = 27 * 28 = 756
                29  addr 3 1 1      r1 += r3    r1 = 756 + 29 = 785
                30  mulr 3 1 1      r1 *= r3    r1 = 785 * 30 = 23550
                31  muli 1 14 1     r1 *= 14    r1 = 23550 * 14 = 329700
                32  mulr 1 3 1      r1 *= r3    r1 = 329700 * 32 = 10550400
                33  addr 4 1 4      r4 += r1    r4 = 968 + 10550400 = 10551368
                34  seti 0 4 0      Zeros out r0
                35  seti 0 0 3      Sets instruction pointer to 0 (jump to JUMP2)

    """
    @opcode
    def sfac(
        self,
        pre: Registers,
        input1: Input,
        input2: Input,  # pylint: disable=unused-argument
        output: Output,
    ) -> None:
        """
        sfac: sum of factors

        sets the output register to the sum of the factors of the register
        specified by "input1" param
        """
        pre[output] = sum(self.factors(pre[input1]))

    def run(
        self,
        program: Program,
        registers: Registers | None = None,
    ) -> Registers:
        """
        Execute the specified program
        """
        # Check first line of program for #ip line
        if program[0][0] != "#ip":
            raise ValueError(
                f"Malformed program. First line must be an instruction "
                f"pointer definition, not {program[0][0]!r}"
            )

        registers: Registers = registers or [0, 0, 0, 0, 0, 0]
        ip: int = program[0][1]
        ptr: int = registers[ip]

        # Discard instruction pointer definition
        program = program[1:]

        while True:
            try:
                instruction: Instruction = program[ptr]
            except IndexError:
                # Instruction pointer is pointing outside the bounds of the
                # program, the program will now exit.
                break

            # Write instruction ptr to ip register
            registers[ip] = ptr

            # Run the instruction
            getattr(self, instruction[0])(registers, *instruction[1:])

            # Write the value of the ip register back the instruction pointer
            ptr = registers[ip]

            # Point at the next instruction
            ptr += 1

        return tuple(registers)


class AOC2018Day19(AOC):
    """
    Day 19 of Advent of Code 2018
    """
    example_data: str = textwrap.dedent(
        """
        #ip 0
        seti 5 0 1
        seti 6 0 2
        addi 0 1 0
        addr 1 2 3
        setr 1 0 0
        seti 8 0 4
        seti 9 0 5
        """
    )

    validate_part1: int = 6

    emu: EmulatorV2 = EmulatorV2()

    # Set by post_init
    program = None

    def post_init(self) -> None:
        """
        Load the program contents, converting the numeric values into integers
        """
        self.program: Program = tuple(
            (params[0], *(int(i) for i in params[1:]))
            for params in (line.split() for line in self.input.splitlines())
        )

    @staticmethod
    def optimize_program(program: Program) -> Program:
        """
        Replace inefficient looping logic used to derive factors with a new
        opcode function
        """
        program = list(program)
        # Replace the double-loop with our new opcode function
        program[2] = ("sfac", 4, 0, 0)
        # This will move to the instruction that exits the program
        program[3] = ("seti", 15, 0, 3)
        return tuple(program)

    def part1(self) -> int:
        """
        Run the program with all registers set to 0
        """
        return self.emu.run(self.program)[0]

    def part1_alt(self) -> int:
        """
        Alternate solution using program optimizations added for Part 2
        """
        return self.emu.run(self.optimize_program(self.program))[0]

    def part2(self) -> int:
        """
        Run optimized program to work around inefficient looping
        """
        return self.emu.run(
            self.optimize_program(self.program),
            registers=[1, 0, 0, 0, 0, 0]
        )[0]


if __name__ == '__main__':
    aoc = AOC2018Day19()
    aoc.run()
