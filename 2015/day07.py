#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/7
'''
import functools
import re
import textwrap

# Local imports
from aoc import AOC


class Circuit:
    '''
    Represents a circuit. The signal provided to a given wire can be obtained
    by index of the Circuit instance.
    '''
    def __init__(self):
        '''
        Initialize an empty circuit
        '''
        self.__components = {}
        self.__gate_pat = re.compile(
            r'^(?:([a-z]+|\d+) )?(AND|OR|(?:L|R)SHIFT|NOT) ([a-z]+|\d+)$'
        )

    @functools.lru_cache
    def __getitem__(self, wire: str) -> int:
        '''
        Return the signal for a given wire, calculating other values as needed
        '''
        value = self.__components[wire]
        if isinstance(value, int):
            # Wire's value is an integer
            return value
        if re.match(r'^[a-z]+$', value):
            # Wire accepts input of another wire
            return self[value]

        signal1, gate, signal2 = self.__gate_pat.match(value).groups()
        if signal1 is not None:
            try:
                signal1 = int(signal1)
            except ValueError:
                signal1 = self[signal1]
        try:
            signal2 = int(signal2)
        except ValueError:
            signal2 = self[signal2]

        match gate:
            case 'AND':
                return signal1 & signal2
            case 'OR':
                return signal1 | signal2
            case 'LSHIFT' | 'RSHIFT':
                return signal1 << signal2 \
                    if gate == 'LSHIFT' \
                    else signal1 >> signal2
            case 'NOT':
                return ~signal2 & 0xffff
            case _:
                raise ValueError('Unsupported gate: {gate!r}')

    def clear_cache(self):
        '''
        Clear cached wire values
        '''
        return self.__getitem__.cache_clear()  # pylint: disable=no-member

    def add_wire(
        self,
        name: str,
        value: str | int,
    ) -> None:
        '''
        Add/replace a wire
        '''
        if not re.match(r'^[a-z]+$', name):
            raise ValueError(f'Invalid wire name: {name!r}')

        try:
            self.__components[name] = int(value)
        except ValueError:
            self.__components[name] = value

    def add_gate(
        self,
        name: str,
        value: str,
    ) -> None:
        '''
        Add/replace a gate
        '''
        if not re.match(r'^[a-z]+$', name):
            raise ValueError(f'Invalid gate name: {name!r}')
        if not self.__gate_pat.match(value):
            raise ValueError(f'Invalid gate operation: {value!r}')

        self.__components[name] = value

    def add(self, definition: str) -> None:
        '''
        Add a wire or gate using circuit definition notation
        '''
        try:
            value, name = definition.split(' -> ')
        except (AttributeError, ValueError):
            pass
        else:
            if re.match(r'^(?:[a-z]+|\d+)$', value):
                return self.add_wire(name, value)
            if self.__gate_pat.match(value):
                return self.add_gate(name, value)

        raise ValueError(f'Invalid circuit component: {value!r}')


class AOC2015Day7(AOC):
    '''
    Day 7 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        123 -> x
        456 -> y
        x AND y -> d
        x OR y -> e
        x LSHIFT 2 -> f
        y RSHIFT 2 -> g
        NOT x -> h
        NOT y -> i
        '''
    )

    validate_part1: int = 65412

    # Set by post_init
    circuit = None

    def post_init(self) -> None:
        '''
        Setup the Circuit
        '''
        self.circuit: Circuit = Circuit()
        for line in self.input.splitlines():
            self.circuit.add(line)

    def part1(self) -> int:
        '''
        Return the number of strings which are nice under Part 1's rules
        '''
        return self.circuit['h'] if self.example else self.circuit['a']

    def part2(self) -> int:
        '''
        Return the number of strings which are nice under Part 2's rules
        '''
        self.circuit.add_wire('b', self.circuit['a'])
        self.circuit.clear_cache()
        return self.circuit['a']

if __name__ == '__main__':
    aoc = AOC2015Day7()
    aoc.run()
