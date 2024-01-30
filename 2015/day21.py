#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/21
'''
import itertools
import math
from collections.abc import Iterator
from dataclasses import dataclass

# Local imports
from aoc import AOC


@dataclass
class Combatant:
    '''
    Represents the stats for a combatant
    '''
    hit_points: int
    damage: int
    armor: int

    def defeats(self, other: 'Combatant') -> bool:
        '''
        Returns True if this combatant would defeat the other combatant,
        otherwise False.
        '''
        def turns_to_win(c1: 'Combatant', c2: 'Combatant') -> int:
            '''
            Given two Combatant objects, calculate the damage done per turn,
            and return the number of turns needed to reduce the other
            combatant's hit points to zero.
            '''
            damage = c1.damage - c2.armor
            if damage < 1:
                # At a minimum damage of 1, the number of turns to win is equal
                # to the number of the enemy combatant's hit points.
                return c2.hit_points
            return math.ceil(c2.hit_points / damage)

        return turns_to_win(self, other) <= turns_to_win(other, self)


class AOC2015Day21(AOC):
    '''
    Day 21 of Advent of Code 2015
    '''
    hit_points = 100

    # Cost, damage rating, and armor rating for each item
    weapons = (
        (8, 4, 0),
        (10, 5, 0),
        (25, 6, 0),
        (40, 7, 0),
        (74, 8, 0),
    )

    armor = (
        (13, 0, 1),
        (31, 0, 2),
        (53, 0, 3),
        (75, 0, 4),
        (102, 0, 5),
        # Simulate no armor equipped
        (0, 0, 0),
    )

    rings = (
        (25, 1, 0),
        (50, 2, 0),
        (100, 3, 0),
        (20, 0, 1),
        (40, 0, 2),
        (80, 0, 3),
        # Include two rings with all zeros to simulate no ring equipped
        (0, 0, 0),
        (0, 0, 0),
    )

    def post_init(self) -> None:
        '''
        Load the boss' data from the input
        '''
        self.boss: Combatant = Combatant(
            *(
                int(line.split()[-1])
                for line in self.input.splitlines()
            )
        )

    @property
    def combatants(self) -> Iterator[tuple[Combatant, int]]:
        '''
        Generator function to return all possible combatants, as well as the
        cost required to outfit each combatant
        '''
        for weapon_cost, weapon_damage, _ in self.weapons:
            for armor_cost, _, armor_defense in self.armor:
                for ring1, ring2 in itertools.combinations(self.rings, 2):
                    yield Combatant(
                        hit_points=self.hit_points,
                        damage=weapon_damage + ring1[1] + ring2[1],
                        armor=armor_defense + ring1[2] + ring2[2],
                    ), weapon_cost + armor_cost + ring1[0] + ring2[0]

    def part1(self) -> int:
        '''
        Return the least amount of gold that can be used to outfit a combatant
        that will defeat the boss.
        '''
        return min(
            cost for combatant, cost in self.combatants
            if combatant.defeats(self.boss)
        )

    def part2(self) -> int:
        '''
        Return the most amount of gold that can be used to outfit a combatant
        that will be defeated by the boss.
        '''
        return max(
            cost for combatant, cost in self.combatants
            if not combatant.defeats(self.boss)
        )


if __name__ == '__main__':
    aoc = AOC2015Day21()
    aoc.run()
