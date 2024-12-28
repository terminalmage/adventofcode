#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/24
'''
import itertools
import textwrap
from collections.abc import Iterator
from typing import Callable, Literal, Never

# Local imports
from aoc import AOC

# Type hints
Signal = Literal[0, 1]
Operation = Callable[[int, int], int]


class Wire:
    '''
    Represents a Wire. When used in conjunction with a Gate, the Gate will add
    itself to the Wire's gates, so that when the Wire's "value" attribute is
    set, its associated Gate is activated.
    '''
    def __init__(self, name: str) -> Never:
        '''
        Initialize a wire object
        '''
        self.name: str = name
        self.gates: set['Gate'] = set()
        # Must be assigned after self.gates due to __setattr__ behavior
        self.value: Signal | None = None

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Wire(name={self.name!r}, value={self.value})'

    def __setattr__(self, name: str, value: Signal):
        '''
        Trigger Gate activation when the .value attribute is set
        '''
        super().__setattr__(name, value)
        if name == 'value':
            gate: 'Gate'
            for gate in self.gates:
                gate.activate()


class Gate:
    '''
    Simulate a gate
    '''
    def __init__(
        self,
        operation: str,
        input1: Wire,
        input2: Wire,
        output: Wire,
    ) -> Never:
        '''
        Represents a logic gate
        '''
        match operation:
            case 'AND':
                self.__op: Operation = int.__and__
            case 'OR':
                self.__op: Operation = int.__or__
            case 'XOR':
                self.__op: Operation = int.__xor__
            case _:
                raise ValueError(f'Invalid operation {operation!r}')

        # If this is a pair of xNN and yNN wires, normalize their order such
        # that X will always be first. This will help for Part 2.
        if {wire.name[0] for wire in (input1, input2)} == {'x', 'y'}:
            if input1.name.startswith('y'):
                input1, input2 = input2, input1

        # Set the inputs and outputs
        self.operation: str = operation
        self.input1: Wire = input1
        self.input2: Wire = input2
        self.output: Wire = output

        # Set the Wire's references to this Gate
        self.input1.gates.add(self)
        self.input2.gates.add(self)

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return (
            f'Gate({self.input1.name} {self.operation} {self.input2.name} '
            f'-> {self.output.name})'
        )

    @property
    def inputs(self) -> tuple[Wire, Wire]:
        '''
        Returns both input1 and input2 as a tuple
        '''
        return self.input1, self.input2

    @property
    def has_xy_input(self) -> bool:
        '''
        Returns True if this gate has xNN/yNN inputs, otherwise False
        '''
        # NOTE: This works because the __init__ normalizes xNN/yNN inputs such
        # that xNN is always input1 and yNN is always input2.
        return (
            self.input1.name.startswith('x')
            and self.input2.name.startswith('y')
        )

    @property
    def has_z_output(self) -> bool:
        '''
        Returns True if this gate has a zNN output, otherwise False
        '''
        return self.output.name.startswith('z')

    def activate(self) -> Never:
        '''
        Perform the specified operation, if the inputs are set and the output
        has not been set.
        '''
        if (
            self.output.value is None
            and self.input1.value is not None
            and self.input2.value is not None
        ):
            self.output.value = self.__op(self.input1.value, self.input2.value)


class Adder:
    '''
    Initialize a series of Wires and Gates, based on the puzzle input
    '''
    def __init__(self, puzzle_input: str) -> Never:
        '''
        Parse the input and set up all wires and logic gates
        '''
        values: str
        gate_defs: str
        values, gate_defs = map(
            str.splitlines,
            puzzle_input.split('\n\n')
        )
        self.values: dict[str, int] = {
            x.rstrip(':'): int(y)
            for x, y in (line.split() for line in values)
        }
        self.gate_defs: tuple[str, ...] = tuple(gate_defs)

        self.wires: dict[str, Wire] = {}
        self.gates: set[Gate] = set()

        self.reset()

    @property
    def and_gates(self) -> Iterator[Gate]:
        '''
        Yields a sequence of all AND gates
        '''
        return (x for x in self.gates if x.operation == 'AND')

    @property
    def or_gates(self) -> Iterator[Gate]:
        '''
        Yields a sequence of all OR gates
        '''
        return (x for x in self.gates if x.operation == 'OR')

    @property
    def xor_gates(self) -> Iterator[Gate]:
        '''
        Yields a sequence of all XOR gates
        '''
        return (x for x in self.gates if x.operation == 'XOR')

    def reset(self) -> Never:
        '''
        Parse the input
        '''
        # Clear the current
        self.wires.clear()
        self.gates.clear()

        gate_def: str
        for gate_def in self.gate_defs:
            operation: str
            input1: str
            input2: str
            output: str
            input1, operation, input2, _, output = gate_def.split()

            # Initialize all Wires
            for wire in (input1, input2, output):
                if wire not in self.wires:
                    self.wires[wire] = Wire(name=wire)

            # Initialize all Gates
            self.gates.add(
                Gate(
                    operation=operation,
                    input1=self.wires[input1],
                    input2=self.wires[input2],
                    output=self.wires[output],
                )
            )

    def run(self) -> int:
        '''
        Apply the values and let the Wires and Gates do their thing
        '''
        self.reset()

        # pylint was returning a false warning for the below line
        wire_name: str  # pylint: disable=unreachable
        value: int
        for wire_name, value in self.values.items():
            self.wires[wire_name].value = value

        # Put all the z-output values in order of their z-index
        bits: list[Signal] = []
        index: int
        for index in itertools.count():
            try:
                bits.append(self.wires[f'z{str(index).zfill(2)}'].value)
            except KeyError:
                break

        # Join the bits into a single string and treat this as a binary number
        return int(''.join(str(bit) for bit in reversed(bits)), 2)

class AOC2024Day24(AOC):
    '''
    Day 24 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        x00: 1
        x01: 0
        x02: 1
        x03: 1
        x04: 0
        y00: 1
        y01: 1
        y02: 1
        y03: 1
        y04: 1

        ntg XOR fgs -> mjb
        y02 OR x01 -> tnw
        kwq OR kpj -> z05
        x00 OR x03 -> fst
        tgd XOR rvg -> z01
        vdt OR tnw -> bfw
        bfw AND frj -> z10
        ffh OR nrd -> bqk
        y00 AND y03 -> djm
        y03 OR y00 -> psh
        bqk OR frj -> z08
        tnw OR fst -> frj
        gnj AND tgd -> z11
        bfw XOR mjb -> z00
        x03 OR x00 -> vdt
        gnj AND wpb -> z02
        x04 AND y00 -> kjc
        djm OR pbm -> qhw
        nrd AND vdt -> hwm
        kjc AND fst -> rvg
        y04 OR y02 -> fgs
        y01 AND x02 -> pbm
        ntg OR kjc -> kwq
        psh XOR fgs -> tgd
        qhw XOR tgd -> z09
        pbm OR djm -> kpj
        x03 XOR y03 -> ffh
        x00 XOR y04 -> ntg
        bfw OR bqk -> z06
        nrd XOR fgs -> wpb
        frj XOR qhw -> z04
        bqk OR frj -> z07
        y03 OR x01 -> nrd
        hwm AND bqk -> z03
        tgd XOR rvg -> z12
        tnw OR pbm -> gnj
        '''
    )

    validate_part1: int = 2024

    def part1(self) -> int:
        '''
        Calculate the number represented by the zNN wires
        '''
        adder: Adder = Adder(self.input)
        return adder.run()

    def part2(self) -> str:
        '''
        Surprise! This is actually a Ripple-Carry Adder with four swapped
        outputs (i.e. 8 incorrect outputs). Determine which outputs were
        swapped.

        https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder

        This adder works from right to left. xNN wires represent the lvalue of
        the addition, while yNN wires represent the rvalue of the addition. zNN
        wires represent the sum of the addition. This is base-2 additon with
        carrying. Any zₙ bit can be calculated as follows:

            zₙ = sumₙ XOR carryₙ
            sumₙ = xₙ XOR yₙ
            carryₙ = (xₙ₋₁ AND yₙ₋₁) OR (sumₙ₋₁ AND carryₙ₋₁)

        That is, zₙ is equal to xₙ XOR yₙ XOR carryₙ, where carryₙ is the carry
        bit from the previous column. sumₙ and carryₙ are represented in this
        system by the intermediate wires. Any operation that doesn't terminate
        in a zNN wire is also represented by an intermediate wire. So...

            1. The AND operations above are represented by intermediate wires.
            2. The OR operation above takes two intermediate wires as input,
               and outputs to an intermediate wire (with one exception, more on
               this below).

        Think of an XOR gate like performing base-2 addition for a given pair
        of bits:

            1. When both corresponding bits are 0, the result is 0.
            2. When both corresponding bits are 1, the result is 0. (and a 1 is
               carried into the next column)
            3. When one bit is 1 and the other is 0, the result is 1.

        For carrying bits, the logic is a bit more complex. This is because
        whether or not a carry bit is 1 or 0 depends on the results of all
        prior columns' sums and carries. To explain this in base-10 math for
        easier understanding, if you are doing addition with carrying, whether
        or not a given column carries over into the next can be affected by
        changing numbers in columns to the right. For example, look at the two
        sums below. In the second one, the ones column was changed in such a
        way that we needed to carry a 1 into the next column. This caused that
        column to also need to carry a 1 into the next.

        Carry         11           1111
        L-value        4847         4847
        R-value      + 9351       + 9357
        ------------------------------------
                      14198        14204

        Moving back to base-2, let's look again at the formula for carryₙ:

            carryₙ = (xₙ₋₁ AND yₙ₋₁) OR (sumₙ₋₁ AND carryₙ₋₁)

        This is derived from the following truths:

            1. A column will receive a carried 1 if both of the prior column's
               values are 1. That is, 1 + 1 = 10, or 0 with a 1 carrying into
               the next column.

            2. A column will receive a carried 1 if the xNN/yNN from the prior
               column contained a 1 and a 0 (i.e. their sum is 1), and the
               prior column received a carried 1.

            3. A bitwise AND will result in a 1 only if both values are 1,
               while an OR will result in a 1 if _either_ of its operands is 1.

        Nothing can be carried into the first column, since nothing came before
        it. Thus, calculating the value of z00 is simply x00 XOR y00. This
        makes x00 XOR y00 the only case of xNN XOR yNN which is allowed to have
        a zNN output. All others must follow the "xNN XOR yNN XOR carryNN"
        pattern. Note that z00 still does follow this pattern, but as nothing
        is being carried in, it's x00 XOR y00 XOR 0 (i.e. x00 + y00 + 0), which
        is the same as x00 XOR y00.

        Just as nothing can be carried into the first column, the last column
        exists merely to receive the final carry bit. This can be confirmed by
        analysis of the puzzle input; there are no references to x45 or y45,
        only z45. Just as in the base-10 addition example above, where adding
        two 4-digit numbers can create a 5-digit number if the leftmost column
        results in a carry, our puzzle input adds 2 44-digit base-2 numbers,
        with z45 holding the carry from x44 + y44.

        The logic for calculating the final z-output is therefore simplified
        from the others. Since there are no xNN/yNN wires for that z-output,
        you can substitute a 0 in their place, making zₘₐₓ₍ₙ₎ equivalent to the
        following:

            zₘₐₓ₍ₙ₎ = 0 XOR carryₘₐₓ₍ₙ₎

        ... which is just the same thing as:

            zₘₐₓ₍ₙ₎ = carryₘₐₓ₍ₙ₎

        More precisely, this would be

            (xₘₐₓ₍ₙ₎₋₁ AND yₘₐₓ₍ₙ₎₋₁) OR (sumₘₐₓ₍ₙ₎₋₁ AND carryₘₐₓ₍ₙ₎₋₁)

        Thus, for the last (and _only_ the last) z-output, the logic gate would
        be an OR, with the operands being two intermediate wires that are
        themselves the result of AND gates.

        Another simplification can be made in calculating z01. From the
        formulas above:

            z₁ = sum₁ XOR carry₁
            sum₁ = x₁ XOR y₁
            carry₁ = (x₀ AND y₀) OR (sum₀ AND carry₀)

        carry₀ will always be 0, because nothing carries into the first column.
        This means that (sum₀ AND carry₀) cannot possibly evaluate as 1,
        meaning that the OR is entirely superfluous. It would be the same thing
        as if one were to write the pseudocode "if X or False". The outcome is
        entirely determined on the outcome of X (in this case the left side of
        the OR). Thus, carry₁ is expressed simply as (x₀ AND y₀). For the
        purposes of the puzzle, that means that the outcome of (x₀ AND y₀) does
        _not_ feed into an OR gate, instead going directly into the XOR gate
        which produces z01.
        '''
        adder: Adder = Adder(self.input)

        last_z: Gate
        *_, last_z = sorted(
            (
                gate for gate in adder.gates
                if gate.output.name.startswith('z')
            ),
            key=lambda gate: int(gate.output.name[1:])
        )

        gates_by_output: dict[str, Gate] = {
            gate.output.name: gate for gate in adder.gates
        }

        swapped: set[Gate] = set()

        for gate in adder.gates:

            match gate.operation:
                case 'XOR':
                    if gate.has_xy_input:
                        if gate.has_z_output and gate.input1.name != 'x00':
                            # The only gate in the format "xNN XOR yNN -> zNN"
                            # which is permitted is: x00 XOR y00 -> z00. See
                            # docstring for a more thorough explanation.
                            swapped.add(gate)
                            continue
                        if not gate.has_z_output:
                            # This is an XOR gate with xNN/yNN inputs, which is
                            # _not_ x00 XOR y00. This means that its output
                            # will be an intermediate wire (i.e. a "sum" wire)
                            # used in determining the carry bit for the next
                            # column. Therefore, search the other gates for an
                            # AND gate which has the current gate as one of its
                            # inputs.
                            and_gate: Gate
                            for and_gate in adder.and_gates:
                                if gate.output in and_gate.inputs:
                                    # We've found a match, we can stop looking
                                    break
                            else:
                                # No match found
                                swapped.add(gate)
                                continue

                    elif not gate.has_z_output:
                        # XOR operations should only happen when doing one of
                        # two things:
                        #
                        #   1. Adding xNN and yNN values
                        #   2. Adding the carry bit to an xNN/yNN sum (with
                        #      output going to a zNN wire)
                        #
                        # If the inside of this elif has been reached, we know
                        # that this XOR gate is not adding an xNN/yNN pair, and
                        # the output for this gate is not zNN. Therefore it
                        # does not match the criteria and needs to be swapped.
                        swapped.add(gate)
                        continue

                case 'AND':
                    if gate.has_z_output:
                        # z-output gates are always either XOR or OR
                        # operations, if we see an AND then it is invalid.
                        swapped.add(gate)
                        continue

                    if gate.has_xy_input:
                        # With one exception (see the docstring above for a
                        # more detailed explanation), "xNN AND yNN" is only
                        # valid as part of the process of determining a carry
                        # bit. The output should be an intermediate wire which
                        # is an input to an OR gate, unless it outputs into a
                        # gate which itself outputs to z01. Therefore, search
                        # the other gates for an OR gate which has the current
                        # gate as one of its inputs.
                        if gate.output not in gates_by_output['z01'].inputs:
                            or_gate: Gate
                            for or_gate in adder.or_gates:
                                if gate.output in or_gate.inputs:
                                    # We've found a match, we can stop looking
                                    break
                            else:
                                # No match found
                                swapped.add(gate)
                                continue

                case 'OR':
                    # The only z-output which is the result of an OR gate is
                    # the final one (see the docstring above for a more
                    # detailed explanation). Any other z-output gate is
                    # invalid.
                    if gate.has_z_output and gate is not last_z:
                        swapped.add(gate)
                        continue

                case _:
                    # The puzzle input should not contain gates that are not
                    # covered in the above cases.
                    raise ValueError(f'Invalid operation {gate.operation}')

        assert len(swapped) == 8, swapped

        return ','.join(sorted(x.output.name for x in swapped))


if __name__ == '__main__':
    aoc = AOC2024Day24()
    aoc.run()
