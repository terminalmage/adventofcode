#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/25
'''
from __future__ import annotations
import re
import textwrap
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Literal

# Local imports
from aoc import AOC

Blueprint = str


@dataclass
class Action:
    '''
    Describes the actions to take for a given state
    '''
    new_value: int
    move: Literal[-1, 1]
    next_state: str

    def __post_init__(self) -> None:
        '''
        Validate move value
        '''
        if self.move not in (-1, 1):
            raise ValueError(f'Invalid move value: {self.move!r}')


class TuringMachine:
    '''
    Implement the behavior defined in the Blueprint
    '''
    def __init__(self, blueprint: Blueprint) -> None:
        '''
        Load the Blueprint
        '''
        lines: list[str] = blueprint.splitlines()[:2]
        self.begin: str = re.match(r'Begin in state ([A-Z])', lines[0]).group(1)
        self.steps: int = int(re.search(r'(\d+)', lines[1]).group(1))
        self.states: dict = defaultdict(dict)

        state_def: tuple[str, ...]
        for state_def in re.findall(
            '\n'.join((
                r'In state ([A-Z]):',
                r'  If the current value is (\d+).',
                r'    - Write the value (\d+).',
                r'    - Move one slot to the (right|left).',
                r'    - Continue with state ([A-Z]).',
                r'  If the current value is (\d+).',
                r'    - Write the value (\d+).',
                r'    - Move one slot to the (right|left).',
                r'    - Continue with state ([A-Z]).',
            )),
            blueprint,
        ):
            for index in range(1, len(state_def), 4):
                if_val, new_value, move, next_state = state_def[index:index + 4]
                self.states[state_def[0]][int(if_val)] = Action(
                    new_value=int(new_value),
                    move=-1 if move == 'left' else 1,
                    next_state=next_state,
                )

    def run(self) -> int:
        '''
        Run through the blueprint and return the number of 1s produced
        '''
        tape: dict[int, int] = defaultdict(int)
        index: int = 0
        state: str = self.begin

        for _ in range(self.steps):
            current_value: int = tape[index]
            action: Action = self.states[state][current_value]
            tape[index] = action.new_value
            index += action.move
            state = action.next_state

        return Counter(tape.values())[1]


class AOC2017Day25(AOC):
    '''
    Day 25 of Advent of Code 2017
    '''
    example_data: str = textwrap.dedent(
        '''
        Begin in state A.
        Perform a diagnostic checksum after 6 steps.

        In state A:
          If the current value is 0:
            - Write the value 1.
            - Move one slot to the right.
            - Continue with state B.
          If the current value is 1:
            - Write the value 0.
            - Move one slot to the left.
            - Continue with state B.

        In state B:
          If the current value is 0:
            - Write the value 1.
            - Move one slot to the left.
            - Continue with state A.
          If the current value is 1:
            - Write the value 1.
            - Move one slot to the right.
            - Continue with state A.
        '''
    )

    validate_part1: int = 3

    def part1(self) -> int:
        '''
        Run the Blueprint and return the number of 1s on the resulting "tape"
        '''
        machine: TuringMachine = TuringMachine(self.input)
        return machine.run()


if __name__ == '__main__':
    aoc = AOC2017Day25()
    aoc.run()
