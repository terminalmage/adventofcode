#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/3
'''
import math
import re
import textwrap

# Local imports
from aoc import AOC


class Item:
    '''
    Base class for a single item on the engine schematic

    NOTE: This class assumes that items cannot span multiple lines.
    '''
    def __init__(self, label: str, row: int, span: tuple[int, int]) -> None:
        '''
        Initialize the object
        '''
        self.label: str = label
        self.row: int = row
        self.span: tuple[int, int] = span

    def __repr__(self) -> str:
        '''
        String representation of class instance
        '''
        return f'Item({self.label!r}, row={self.row}, span={self.span})'

    def adjacent_to(self, other: 'Item') -> bool:
        '''
        Returns True if this Item is adjacent to the other Item, otherwise
        False
        '''
        # If the items are more than a line apart, they cannot be adjacent
        if abs(self.row - other.row) > 1:
            return False

        other_cols: set[int] = set(range(*other.span))

        if self.row == other.row:
            # Other item is on the same line. neighbor_cols represents the cols
            # that the other item must contain to be considered adjacent.
            neighbor_cols = {self.span[0] - 1, self.span[1]}
            # If the set union is not empty, the other item occupies one of the
            # two neighbor columns and is therefore adjacent.
            return bool(other_cols & neighbor_cols)

        # If we've reached this point, then the other item is on the row above
        # or below this item. To check adjacency, we can simply do a set union
        # check to see if the other item's span encompasses a range of columns
        # that run from the column before the beginning to the column after
        # the end.
        return bool(other_cols & set(range(self.span[0] - 1, self.span[1] + 1)))


class AOC2023Day3(AOC):
    '''
    Day 3 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        '''
    )

    validate_part1: int = 4361
    validate_part2: int = 467835

    def post_init(self) -> None:
        '''
        Read in the engine document
        '''
        self.numbers: list[Item] = []
        self.symbols: list[Item] = []

        number_re: re.Pattern = re.compile(r'\d+')
        symbol_re: re.Pattern = re.compile(r'[^\d.]')

        row: int
        line: str
        for row, line in enumerate(self.input.splitlines()):
            self.numbers.extend(
                Item(number.group(0), row, number.span(0))
                for number in number_re.finditer(line)
            )
            self.symbols.extend(
                Item(symbol.group(0), row, symbol.span(0))
                for symbol in symbol_re.finditer(line)
            )

    def part1(self) -> int:
        '''
        Return the sum of part numbers
        '''
        return sum(
            int(number.label) for number in self.numbers
            if any(number.adjacent_to(symbol) for symbol in self.symbols)
        )

    def part2(self) -> int:
        '''
        Return the sum of the gear ratios for all gears
        '''
        total: int = 0

        symbol: Item
        for symbol in self.symbols:
            if symbol.label == '*':
                gear_neighbors: list[int] = [
                    int(number.label) for number in self.numbers
                    if symbol.adjacent_to(number)
                ]
                if len(gear_neighbors) == 2:
                    total += math.prod(gear_neighbors)

        return total


if __name__ == '__main__':
    aoc = AOC2023Day3()
    aoc.run()
