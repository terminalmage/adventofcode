#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/22
'''
import copy
import itertools
import math

# Local imports
from aoc import AOC

# Typing shortcuts
Spell = list[int]


class AOC2015Day22(AOC):
    '''
    Day 22 of Advent of Code 2015
    '''
    hit_points = 50
    mana = 500

    spells = (
        # Mana cost, damage, heal, shield, mana refresh, effect length
        [53, 4, 0, 0, 0, 1],
        [73, 2, 2, 0, 0, 1],
        [113, 0, 0, 7, 0, 6],
        [173, 3, 0, 0, 0, 6],
        [229, 0, 0, 0, 101, 5],
    )

    # Set by post_init
    boss_hit_points = None
    boss_damage = None

    def post_init(self) -> None:
        '''
        Load the boss' configuration from the input
        '''
        self.boss_hit_points: int
        self.boss_damage: int
        self.boss_hit_points, self.boss_damage = (
            int(line.split()[-1])
            for line in self.input.splitlines()
        )

    def simulate(
        self,
        spell: Spell,
        hit_points: int | None = None,
        boss_hit_points: int | None = None,
        current_mana: int | None = None,
        mana_spent: int = 0,
        effects: list[Spell] | None = None,
        wins: set[int] | None = None,
        hard_mode: bool = False,
    ) -> None:
        '''
        Recursively simulate all possible paths, from a given battle state.
        Aggregate the total mana spent for all winning conditions
        '''
        hit_points: int = hit_points or self.hit_points
        boss_hit_points: int = boss_hit_points or self.boss_hit_points
        current_mana: int = current_mana or self.mana
        effects: list[Spell] = effects or []
        wins: set[int] = wins or {math.inf}

        # Ignore spells which have active effects; they cannot be run again
        # while the effect is active. When comparing the desired spell to the
        # list of spells with effects, we are comparing copies of the data
        # structures for each spells. Since the last element of the list is
        # used to contain the remaining effect length (and is decremented each
        # turn), list slices excluding the last element are used for
        # comparisons. If all values besides the last one are the same, then
        # we know it's the same spell since none of the spells have identical
        # values.
        if spell[:-1] in (e[:-1] for e in effects if e[-1] > 1):
            return wins

        def apply_spells(*spells: Spell) -> list[Spell]:
            '''
            Apply any effects from the specified spells
            '''
            nonlocal boss_hit_points
            nonlocal hit_points
            nonlocal shield
            nonlocal current_mana
            # Damage to boss
            boss_hit_points -= sum(s[1] for s in spells)
            # Healing
            hit_points += sum(s[2] for s in spells)
            # Shield
            shield += sum(s[3] for s in spells)
            # Mana recharge
            current_mana += sum(s[4] for s in spells)
            # Decrement effect length
            for s in spells:
                s[-1] -= 1

            return [s for s in spells if s[-1]]

        ###############################################################
        # WIZARD'S TURN
        ###############################################################

        # Reset shield (if shield spell is active, it will be reset when spells
        # are applied directly below)
        shield: int = 0

        if hard_mode:
            hit_points -= 1
            if hit_points <= 0:
                # Wizard has been defeated
                return wins

        # Apply active spell effects
        effects = apply_spells(*effects)

        # Spend mana
        current_mana -= spell[0]
        mana_spent += spell[0]

        # If the wizard runs out of mana, the battle is lost. if the total mana
        # spent is greater than the lowest amount spent in a win, there is no
        # way we can do better. In both cases, there is nothing more to do.
        if current_mana < 0 or mana_spent >= min(wins):
            return wins

        # Spells with an effect duration of more than 1 do not apply until next
        # turn. Therefore, if the effect length is > 1 then add it to the list
        # of effects so that it applied in the next turn.
        if spell[-1] > 1:
            effects.append(copy.deepcopy(spell))
        else:
            apply_spells(spell)

        if boss_hit_points <= 0:
            # Boss has been defeated
            wins.add(mana_spent)
            return wins

        if hit_points <= 0:
            # Wizard has been defeated
            return wins

        ###############################################################
        # BOSS' TURN
        ###############################################################

        # Reset shield (if shield spell is active, it will be reset when spells
        # are applied directly below)
        shield = 0

        # Apply active spell effects
        effects = apply_spells(*effects)

        if boss_hit_points <= 0:
            # Boss has been defeated
            wins.add(mana_spent)
            return wins

        # Apply damage from boss attack
        hit_points -= max(1, self.boss_damage - shield)
        if hit_points <= 0:
            # Wizard has been defeated
            return wins

        # Try again with another spell until the wizard wins or is defeated
        for next_spell in self.spells:
            wins = self.simulate(
                spell=copy.deepcopy(next_spell),
                hit_points=hit_points,
                boss_hit_points=boss_hit_points,
                current_mana=current_mana,
                mana_spent=mana_spent,
                effects=copy.deepcopy(effects),
                wins=wins,
                hard_mode=hard_mode,
            )

        return wins

    def play_game(self, hard_mode: bool = False) -> int:
        '''
        Simulate a game given the starting stats defined as class attributes
        '''
        return min(
            itertools.chain.from_iterable(
                self.simulate(
                    copy.deepcopy(spell),
                    hard_mode=hard_mode,
                ) for spell in self.spells
            )
        )

    def part1(self) -> int:
        '''
        Return the least amount of mana that can be spent in a winning game
        '''
        return self.play_game()

    def part2(self) -> int:
        '''
        Return the least amount of mana that can be spent in a winning game,
        with "hard mode" enabled
        '''
        return self.play_game(hard_mode=True)


if __name__ == '__main__':
    aoc = AOC2015Day22()
    aoc.run()
