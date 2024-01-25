#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/15
'''
import functools
import itertools
import re
import textwrap
from dataclasses import dataclass

# Local imports
from aoc import AOC

@dataclass
class Ingredient:
    '''
    Represents attributes of a given ingredient
    '''
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


class AOC2015Day15(AOC):
    '''
    Day 15 of Advent of Code 2015
    '''
    example_data: str = textwrap.dedent(
        '''
        Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
        Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
        '''
    )

    validate_part1: int = 62842880
    validate_part2: int = 57600000

    def post_init(self) -> None:
        '''
        Load the ingredients
        '''
        ingredient_re: re.Pattern = re.compile(
            r'^(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), '
            r'texture (-?\d+), calories (-?\d+)'
        )

        self.ingredients = tuple(
            Ingredient(
                ingredient.group(1),
                *(int(group) for group in ingredient.groups()[1:])
            )
            for ingredient in (
                ingredient_re.match(line) for line in self.input.splitlines()
            )
        )

    @staticmethod
    def calculate(
        *ingredients: Ingredient,
        calorie_target: int | None = None,
    ) -> int:
        '''
        Calculate the score for a given combination of ingredients. Input
        should be a seqence of 100 Ingredient instances, generated using
        itertools.combinations_with_replacement(). This function will sum up
        the values for the various attributes of each ingredient and then
        multiply them to calculate the score for that combination of
        ingredients.

        If the sum of any of the attributes is a negative number, or if a
        calorie target is specified and the ingredients don't match, the score
        will be zero.
        '''
        if (
            calorie_target is not None
            and sum(item.calories for item in ingredients) != calorie_target
        ):
            return 0

        sums: list[int] = []
        for attr in ('capacity', 'durability', 'flavor', 'texture'):
            subtotal = sum(getattr(item, attr) for item in ingredients)
            if subtotal <= 0:
                return 0
            sums.append(subtotal)
        return functools.reduce(lambda x, y: x * y, sums)

    def part1(self) -> int:
        '''
        Return best possible cookie score
        '''
        return max(
            self.calculate(*combination) for combination in
            itertools.combinations_with_replacement(self.ingredients, 100)
        )

    def part2(self) -> int:
        '''
        Return best possible cookie score for a cookie with 500 calories
        '''
        return max(
            self.calculate(*combination, calorie_target=500) for combination in
            itertools.combinations_with_replacement(self.ingredients, 100)
        )


if __name__ == '__main__':
    aoc = AOC2015Day15()
    aoc.run()
