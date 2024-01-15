#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/12
'''
import copy
import re
from dataclasses import dataclass

# Local imports
from aoc import AOC

Instruction = str
Program = list[Instruction]


@dataclass
class Computer:
    '''
    Simulates a computer, with its four registers
    '''
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0

    def reset(self) -> None:
        '''
        Reset all the registers' values to 0
        '''
        self.a = self.b = self.c = self.d = 0

    def init(self, **init: int) -> None:
        '''
        Reset registers and use any kwargs passed in to set initial values
        '''
        register: str
        value: int

        # Reset all registers to 0
        self.reset()
        # Set initial values
        for register, value in init.items():
            setattr(self, register, value)

    def resolve(self, value: str) -> int:
        '''
        Given a string, return either the value of the matching register, or
        failing that, assume it's a string integer and return the result.
        '''
        try:
            return getattr(self, value)
        except AttributeError:
            return int(value)

    def optimize(self, program: Program) -> Program:  # pylint: disable=too-many-statements
        '''
        Detect loops and optimize them

        MULTIPLICATION
        --------------

            cpy b c
            inc a
            dec c
            jnz c -2
            dec d
            jnz d -5

        The result of this loop will be to multiply the values in registers b
        and d, add the result to register a, and zero out both registers c and
        d. We know this because we execute the outer loop until d == 0 (in
        other words, "d" times), and each time we do so, we take the value from
        register b, load it into register c, and increment register a until
        register c is zero.

        DIVISION (WITH REMAINDER)
        -------------------------

            cpy 2 c
            jnz b 2
            jnz 1 6
            dec b
            dec c
            jnz c -4
            inc a
            jnz 1 -7

        The first instruction in this loop sets c to 2. The next skips the
        third instruction, unless b == 0. The third instruction is therefore
        only reached when b == 0, at which point an unconditional jump is
        executed to exit the loop (i.e. jump one instruction past the end of
        it). The 4th and 5th instructions, decrement registers b and c. If
        register c is nonzero, the sixth instruction jumps back up to the zero
        check for b (instruction 2), otherwise flow proceeds to the seventh
        instruction, which increments register a. After register a is
        incremented, the loop repeats, with an unconditional jump back to the
        top.

        The result is the following:

            - For every 2 times b is decremented, a is incremented.
              - This is equivalent to a floor division of register b by 2,
                adding the result to register a.
              - The value assigned to register c is the divisor; setting it to
                3 would increment a once every 3 times b is decremented (i.e.
                divison by 3).
            - Once b reaches 0, the loop is exited.
              - If b is even, it reaches zero at the end of the inner loop.
                Register c will be reset to 2, but the "jnz b 2" will then exit
                the loop.
              - If b is odd, it reaches zero mid-loop, and register c will
                contain a value of 1
            - Once the loop is complete, register c contains the divisor minus
              the remainder of the division. For example, if dividing by 2 like
              in our example, an even number would leave 2 in register c, while
              an odd number would leave 1 in register c. If dividing by 3, when
              the remainder is 1, register c would contain a value of 2.

        ADDITION
        --------

            dec d
            inc c
            jnz d -2

        This will have the result of increasing the value of register c by the
        value of register d, and zeroing out register d. Note that this kind of
        loop could also be used to subtract, by using a "dec" instead of an
        "inc" here for register c.

        SUBTRACTION
        -----------

            jnz c 2
            jnz 1 4
            dec b
            dec c
            jnz 1 -4

        Subtraction can can also be done via its own type of loop. This loop
        will reduce the value in register b by the value in register c, zeroing
        out register c in the process. Once register c reaches zero, the second
        instruction will finally be executed, jumping outside of the loop.
        '''
        # Make shallow copy of program since we will be modifying instructions
        program: Program = copy.copy(program)

        add: re.Pattern = re.compile(r'^jnz ([abcd]) -2$')
        multiply: re.Pattern = re.compile(r'^jnz ([abcd]) -5$')

        index: int
        instruction: Instruction

        # Detect multiplication loops
        for index, instruction in enumerate(program):
            try:
                outer_reg: str = multiply.match(instruction).group(1)
            except AttributeError:
                # Regex did not match
                continue
            # Sanity check and make sure this fits the optimization pattern
            # (i.e. the same register from the jnz is being decremented each
            # iteration of the outer loop)
            if program[index - 1] != f'dec {outer_reg}':
                continue
            # Now that we've confirmed the outer loop pattern, check for the
            # inner loop.
            cmd: str
            inner_reg: str
            temp_reg: str
            try:
                cmd, inner_reg, temp_reg = program[index - 5].split()
            except ValueError:
                continue
            if cmd != 'cpy':
                continue
            # If we've gotten here, we know that the inner_reg is being copied
            # into the temp_reg each iteration of the outer loop. Confirm that
            # the other commands match the inner loop pattern.
            if program[index - 3:index - 1] != [
                f'dec {temp_reg}',
                f'jnz {temp_reg} -2',
            ]:
                continue
            # Finally, confirm the register that will be increased by this loop
            action: str
            mod_reg: str
            try:
                action, mod_reg = program[index - 4].split()
            except ValueError:
                continue
            if action not in ('inc', 'dec'):
                continue
            # We've now confirmed the structure of the inner and outer loops
            # and can construct our optimized command.
            program[index - 5] = (
                f'mul {inner_reg} {outer_reg} {action} {mod_reg} '
                f'clear {temp_reg}{outer_reg}'
            )
            # Preserve the total number of commands by putting no-op jumps
            # in the other command slots
            for i in range(index - 4, index + 1):
                program[i] = 'jnz 0 0'

        # Detect division loops
        for index, instruction in enumerate(program):
            if instruction == 'jnz 1 -7':
                # Detect the divisor and the remainder register from the top of
                # the loop
                divisor: int
                remainder: str
                try:
                    divisor, remainder = re.match(
                        r'^cpy (\d+) ([abcd])$',
                        program[index - 7],
                    ).groups()
                except AttributeError:
                    # This is not a match for the divison loop
                    continue
                # Detect the dividend register
                try:
                    dividend: str = re.match(
                        r'^jnz ([abcd]) 2$',
                        program[index - 6],
                    ).group(1)
                except AttributeError:
                    # This is not a match for the divison loop
                    continue
                # Make sure the next instruction is our jump out of the loop
                if program[index - 5] != 'jnz 1 6':
                    continue
                # The next two registers should decrement our dividend and
                # remainder registers. The order is not important.
                if sorted(program[index - 4:index - 2]) != sorted(
                    f'dec {reg}' for reg in (dividend, remainder)
                ):
                    continue
                # Find our quotient register
                try:
                    quotient: str = re.match(
                        r'^inc ([abcd])$',
                        program[index - 1],
                    ).group(1)
                except AttributeError:
                    # This is not a match for the divison loop
                    continue

                # We've now confirmed the structure of the inner and outer
                # loops and can construct our optimized command.
                program[index - 7] = (
                    f'div {dividend} {divisor} inc {quotient} '
                    f'rem {remainder} clear {dividend}'
                )
                # Preserve the total number of commands by putting no-op jumps
                # in the other command slots
                for i in range(index - 6, index + 1):
                    program[i] = 'jnz 0 0'

        # Detect addditon/subtraction loops. NOTE: This must be done after
        # multiplication, since a multiplication loop contains an addition loop
        # within it. Optimizing the inner addition loop before multiplication
        # loop detection has been performed will break the program. Yes, I did
        # find out about this the hard way.
        for index, instruction in enumerate(program):
            try:
                temp_reg: str = add.match(instruction).group(1)
            except AttributeError:
                # Regex did not match
                continue
            # Look at the previous two instructions and make sure we have an
            # instruction which decrements that register
            prev: list[Instruction] = program[index - 2:index]
            try:
                prev.remove(f'dec {temp_reg}')
            except ValueError:
                continue
            # Detect the other instruction
            action: str
            mod_reg: str
            try:
                action, mod_reg = prev[0].split()
            except ValueError:
                continue
            # Use no sign for addition and a minus sign for subtraction
            # (subtraction is the same as adding a negative number)
            sign: str
            match action:
                case 'inc':
                    sign = ''
                case 'dec':
                    sign = '-'
                case _:
                    continue
            # We've now confirmed that this matches the characteristics of a
            # single loop. Like we did for double-loops, modify the program and
            # inject an optimized command.
            program[index - 2] = f'add {temp_reg} {sign}{mod_reg}'
            # Preserve the total number of commands by putting no-op jumps in
            # the other command slots
            for i in range(index - 1, index + 1):
                program[i] = 'jnz 0 0'

        # Detect subtraction loops
        for index, instruction in enumerate(program):
            if instruction == 'jnz 1 -4':
                try:
                    rvalue: str = re.match(
                        r'jnz ([abcd]) 2',
                        program[index - 4],
                    ).group(1)
                except AttributeError:
                    # This is not a match for the subtraction loop
                    continue
                # Next, look for the jump out of the loop
                if program[index - 3] != 'jnz 1 4':
                    continue
                # The next two instructions will decrement two registers, the
                # one we already identified as the rvalue, and the one that
                # will be the lvalue.
                decs: list[Instruction] = program[index - 2:index]
                try:
                    # Remove the register we identified as the rvalue. This
                    # will leave a list of length 1, from which we can deduce
                    # the lvalue.
                    decs.remove(f'dec {rvalue}')
                except ValueError:
                    continue
                try:
                    lvalue: str = re.match(
                        r'dec ([abcd])',
                        decs[0],
                    ).group(1)
                except AttributeError:
                    # This is not a match for the subtraction loop
                    continue
                # Make sure the two registers aren't the same
                if lvalue == rvalue:
                    continue
                # We've now confirmed that this matches the structure of a
                # subtraction loop. We can now modify the program and inject an
                # optimized command.
                program[index - 4] = f'sub {lvalue} {rvalue}'
                # Preserve the total number of commands by putting no-op jumps
                # in the other command slots
                for i in range(index - 3, index + 1):
                    program[i] = 'jnz 0 0'

        return program

    def exec(self, index: int, instruction: Instruction) -> int:
        '''
        Execute the specified instruction, and return the index of the next
        instruction to be run.
        '''
        match instruction.split():
            case ['cpy', value, register]:
                value: int
                try:
                    value = int(value)
                except ValueError:
                    # Value is not an int, but rather another register
                    value = getattr(self, value)
                # Set register to the desired value
                setattr(self, register, value)

            case ['inc', register]:
                # Increment register
                setattr(self, register, getattr(self, register) + 1)

            case ['dec', register]:
                # Decrement register
                setattr(self, register, getattr(self, register) - 1)

            case ['jnz', register, value]:
                # Jump forward/backward by the specified number of
                # instructions, but only if the specified register does not
                # contain a value of 0. If the register is not found, it is
                # assumed that the parameter directly after the 'jnz' is an
                # integer value rather than the name of a register.
                register_value: int = self.resolve(register)

                # Jump forward/backward if the value is > 0
                if register_value:
                    return index + self.resolve(value)

            # The following commands are not part of the instruction set, but
            # are rather added by the loop optimization logic.
            case ['mul', reg1, reg2, action, mod_reg, 'clear', clear]:
                # Multiply the two specified registers
                product: int = self.resolve(reg1) * self.resolve(reg2)
                if action == 'dec':
                    product *= -1
                # Add the product to the register we are modifying
                setattr(self, mod_reg, getattr(self, mod_reg) + product)
                # Clear the specified register(s)
                clear_reg: str
                for clear_reg in clear:
                    setattr(self, clear_reg, 0)

            case [
                'div', dividend, divisor, 'inc', mod_reg,
                'rem', rem_reg, 'clear', clear
            ]:
                divisor: int = self.resolve(divisor)
                result: int
                remainder: int
                result, remainder = divmod(self.resolve(dividend), divisor)
                # Add the result to the register we are modifying
                setattr(self, mod_reg, getattr(self, mod_reg) + result)
                # The "remainder" register will have divisor - remainder in it
                # at the end of the division operation.
                setattr(self, rem_reg, divisor - remainder)
                clear_reg: str
                for clear_reg in clear:
                    setattr(self, clear_reg, 0)

            case ['add', reg1, reg2]:
                # Add the value from reg1 into reg2, clearing reg1
                setattr(self, reg2, getattr(self, reg2) + self.resolve(reg1))
                # Clear reg1
                setattr(self, reg1, 0)

            case ['sub', lvalue, rvalue]:
                # Subtract the rvalue from the lvalue, clearing the rvalue
                # register.
                setattr(
                    self, lvalue,
                    self.resolve(lvalue) - self.resolve(rvalue)
                )
                # Clear rvalue
                setattr(self, rvalue, 0)

            case _:
                raise ValueError(f'Invalid command: {instruction!r}')

        # The new index will be the next instruction, unless we jumped above.
        return index + 1

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
            index = self.exec(index, program[index])


class AOC2016Day12(AOC):
    '''
    Day 12 of Advent of Code 2016
    '''
    day = 12

    def __init__(self, example: bool = False) -> None:
        '''
        Initialize the computer and load the program from the puzzle input
        '''
        super().__init__(example=example)
        self.computer: Computer = Computer()
        self.program: Program = self.input.read_text().splitlines()

    def part1(self) -> int:
        '''
        Return the value in register a after the program runs to completion
        '''
        self.computer.run(self.program)
        return self.computer.a

    def part2(self) -> int:
        '''
        Same as part 1, but with register c initialized to 1
        '''
        self.computer.run(self.program, c=1)
        return self.computer.a


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day12(example=True)
    aoc.validate(aoc.part1(), 42)
    # Run against actual data
    aoc = AOC2016Day12(example=False)
    aoc.run()
