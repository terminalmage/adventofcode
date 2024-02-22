#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/14
'''
from __future__ import annotations
import textwrap
from collections.abc import Iterator

# Local imports
from aoc import AOC

Recipe = int
Recipes = tuple[Recipe] | tuple[Recipe, Recipe]


class RecipeTester:
    '''
    Tracks values for recipe-making
    '''
    def __init__(self):
        '''
        Initialize the attributes
        '''
        self.recipes = self.elf1 = self.elf2 = None
        self.reset()

    def reset(self) -> None:
        '''
        Reset values
        '''
        self.recipes: list[int] = [3, 7]
        self.elf1: int = 0
        self.elf2: int = 1

    def iter_recipes(self) -> Iterator[Recipe]:
        '''
        Produces a never-ending sequence of recipes
        '''
        self.reset()

        recipe: Recipe

        while True:
            for recipe in (
                int(n) for n in str(
                    self.recipes[self.elf1] + self.recipes[self.elf2]
                )
            ):
                self.recipes.append(recipe)
                yield recipe

            # Advance both elves to their next position
            self.elf1 = (self.elf1 + self.recipes[self.elf1] + 1) % len(self.recipes)
            self.elf2 = (self.elf2 + self.recipes[self.elf2] + 1) % len(self.recipes)

    def __len__(self) -> int:
        '''
        Return the number of recipes made
        '''
        return len(self.recipes)


class AOC2018Day14(AOC):
    '''
    Day 14 of Advent of Code 2018
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        18
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        51589
        '''
    )

    validate_part1: str = '9251071085'
    validate_part2: int = 9

    def part1(self) -> str:
        '''
        Return the next 10 recipes after the number of recipes defined in the
        puzzle input
        '''
        # Number of practice recipes to make
        practice: int = int(self.input_part1)
        # We need at least 10 more than the number of practice recipes
        target: int = practice + 10

        tester: RecipeTester = RecipeTester()
        recipe_hose: Iterator[Recipe] = tester.iter_recipes()

        while len(tester) < target:
            next(recipe_hose)

        return ''.join(str(n) for n in tester.recipes[practice:target])

    def part2(self) -> int:
        '''
        Return the number of recipes before the sequence defined in the puzzle
        input appears
        '''
        # The target sequence of ints we are looking for
        target: list[int] = [int(n) for n in self.input_part2]
        # Number of digits in the target
        num_digits: int = len(target)
        # Current item in the target that we are trying to match
        index: int = 0

        tester: RecipeTester = RecipeTester()
        recipe_hose: Iterator[Recipe] = tester.iter_recipes()

        # The index will be a pointer to the current item in the target list,
        # which the puzzle input split into a list of integers. If we find a
        # match, increment the index so the next loop iteration will look at
        # the next digit in the target. Otherwise, reset the index to 0. Once
        # the index has reached a value equal to the length of the target, we
        # know we have matched all items, at which point the loop ends.
        while index < num_digits:
            index = (
                0 if next(recipe_hose) != target[index]
                else index + 1
            )

        return len(tester) - num_digits


if __name__ == '__main__':
    aoc = AOC2018Day14()
    aoc.run()
