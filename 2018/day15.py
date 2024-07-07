#!/usr/bin/env python
"""
https://adventofcode.com/2018/day/15
"""
from __future__ import annotations
import copy
import itertools
import textwrap
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal, Sequence

# Local imports
from aoc import AOC, XY, Grid, Directions, directions

READING_ORDER: Directions = (
    directions.NORTH,
    directions.WEST,
    directions.EAST,
    directions.SOUTH,
)
DEFAULT_ELF_ATTACK: int = 3


class ElfVanquished(Exception):
    """
    Used to signal that an Elf has perished
    """

class BattleComplete(Exception):
    """
    Used to signal that combat has ended
    """

class Tiles:
    """
    Defines possible tile values
    """
    WALL: str = "#"
    UNOCCUPIED: str = "."
    GOBLIN: str = "G"
    ELF: str = "E"


@dataclass
class Combatant:
    """
    Base class for combatants
    """
    AP: int = 3
    HP: int = 200

    @property
    def opponent(self) -> type[Combatant]:
        """
        Must be implemented in subclass
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        The string representation of this combatant
        """
        return self.__class__.__name__[0]


class Goblin(Combatant):
    """
    Goblin combatants
    """
    @property
    def opponent(self) -> type[Combatant]:
        """
        Return the type of the opponent
        """
        return Elf


class Elf(Combatant):
    """
    Elf combatants
    """
    @property
    def opponent(self) -> type[Combatant]:
        """
        Return the type of the opponent
        """
        return Goblin


# Type hints
Route = list[XY]
Positions = set[XY]
Tile = Literal[Tiles.WALL, Tiles.UNOCCUPIED, Tiles.GOBLIN, Tiles.ELF]
Opponent = type[Goblin | Elf]


class BattleMap(Grid):
    """
    Simulates map from puzzle
    """
    def __init__(
        self,
        data: Path | str | Sequence[str],
        row_cb: Callable[[str], Any] = lambda col: col,
    ) -> None:
        """
        Load the grid contents, then establish which of the cells contain
        combatants
        """
        super().__init__(data, row_cb, neighbor_order=READING_ORDER)
        self.__orig_state = None
        self.combatants: Positions = set()
        self.unoccupied: Positions = set()

    def mark_unoccupied(self, pos: XY) -> None:
        """
        Mark a tile as unoccupied
        """
        self[pos] = Tiles.UNOCCUPIED
        self.unoccupied.add(pos)

    def move(self, old: XY, new: XY) -> None:
        """
        Move the combatant from the old position to the new one, updating the
        combatant and unoccupied attributes in the process
        """
        if old not in self.combatants:
            raise ValueError(f"Position {old} ({self[old]}) is not a combatant")
        if self[new] != Tiles.UNOCCUPIED:
            raise ValueError(f"Position {new} ({self[new]}) is not unoccupied")

        # Move combatant to the new position
        self[new] = self[old]
        self.combatants.add(new)
        self.combatants.remove(old)
        self.unoccupied.remove(new)

        # Set the old position as unoccupied
        self.mark_unoccupied(old)

    def next_step(self, start: XY) -> XY | None:
        """
        BFS which explores in "reading order". Since multiple paths to a target
        could have the same path length, and these ties are broken by the
        reading order of the position (left to right, up to down), mimicking
        reading order for the BFS traversal ensures that the first candidate
        path to reach the target will be the "winner" of any ties.

        To define "reading order" for the purposes of this BFS, we must
        consider the reading order of the possible moves. Therefore, our
        traversal order is:

          1. north
          2. west
          3. east
          4. south

        Visualized below, you can see the starting point "S", with the 4
        potential cardinal directions labeled 1 through 4.

        #######
        #  1  #
        # 2S3 #
        #  4  #
        #######

        """
        opponents: Positions = {
            xy for xy in self.combatants
            if isinstance(self[xy], self[start].opponent)
        }
        # Build a set of targets consisting of any tile adjacent to an
        # opponent, which is currently unoccupied.
        targets: Positions = {
            coord for coord in itertools.chain.from_iterable(
                (n for n, _ in self.neighbors(opp))
                for opp in opponents
            )
            if coord in self.unoccupied
        }
        #print(sorted(targets)); raise SystemExit
        if not targets:
            return None

        # The order of moves for a given route is a list of coordinates, hence
        # the double brackets used to initialize this deque.
        dq: deque[Route] = deque([[start]])
        visited: set[XY] = {start}
        while dq:
            # Get a route off of the beginning of the queue
            route: Route = dq.popleft()

            # Get the row and column of the last step in the current route
            pos: XY = route[-1]

            # Check if the last step is one of our targets
            if pos in targets:
                # This is the best route to one of the targets, return the
                # first step after the starting point.
                return route[1]

            # Attempt movement in order of directions that optimizes the
            # "reading order" (see the docstring above)
            delta: XY
            for delta in self.directions:
                new_pos: XY = (pos[0] + delta[0], pos[1] + delta[1])
                if new_pos in self.unoccupied and new_pos not in visited:
                    # This is a position we can move to. Add to set of visited
                    # coordinates, and append it to the current route.
                    visited.add(new_pos)
                    dq.append(route + [new_pos])

        # No movements reached any target
        return None

    def attack_target(self, pos: XY) -> XY | None:
        """
        Return the attack target for the combatant at the specified position.
        If no combatant is in range, return None.
        """
        # A list of 3-tuples, one for each in-range opponent. The first element
        # of each is the opponent's HP, and the 2nd and 3rd are the row and
        # column of the opponent's position. In the case of multiple in-range
        # opponents, the one with the fewest HP gets attacked, so organizing
        # the in-range opponents in this way allows for simple tuple sorting to
        # produce the desired target (i.e. the first item in the sorted list).
        in_range: list[tuple[int, int, int]] = sorted([
            (item.HP, *xy) for xy, item in self.neighbors(pos)
            if isinstance(item, self[pos].opponent)
        ])
        try:
            return in_range[0][1:]
        except IndexError:
            # No enemies in range
            return None

    def simulate(
        self,
        elf_attack: int = DEFAULT_ELF_ATTACK,
        elf_deaths_permitted: bool = True,
    ) -> int:
        """
        Simulate battle
        """
        try:
            self.data, self.combatants, self.unoccupied = (
                copy.deepcopy(item) for item in self.__orig_state
            )
        except TypeError as exc:
            self.combatants.clear()
            self.unoccupied.clear()

            pos: XY
            tile: Tile

            for pos, tile in self.tile_iter():
                match tile:
                    case Tiles.GOBLIN:
                        self.combatants.add(pos)
                    case Tiles.ELF:
                        self.combatants.add(pos)
                    case Tiles.UNOCCUPIED:
                        self.unoccupied.add(pos)
                    case Tiles.WALL:
                        pass
                    case _:
                        raise ValueError(
                            f"Expected a valid tile character, not {tile!r}"
                        ) from exc

            self.__orig_state = tuple(
                copy.deepcopy(item)
                for item in (self.data, self.combatants, self.unoccupied)
            )

        for pos in self.combatants:
            match self[pos]:
                case Tiles.GOBLIN:
                    self[pos] = Goblin()
                case Tiles.ELF:
                    self[pos] = Elf(AP=elf_attack)

        completed_rounds: int = 0

        try:
            while True:

                pos: XY
                for pos in sorted(self.combatants):

                    if pos not in self.combatants:
                        # Combatant perished earlier this round
                        continue

                    # End battle if all of the remaining combatants are the
                    # same type. to check this, toss all the types into a set
                    # and check the length of that set. while there are still
                    # both Goblins and Elfs on the battlefield, there should be
                    # 2 items in the set.
                    if len({type(self[c]) for c in self.combatants}) == 1:
                        raise BattleComplete

                    attacker: Goblin | Elf = self[pos]
                    target: XY | None = self.attack_target(pos)

                    if target is None:
                        # Figure out where to move
                        new_pos: XY | None = self.next_step(pos)
                        if new_pos is not None:
                            # Move to the new position
                            self.move(pos, new_pos)
                            target = self.attack_target(new_pos)

                    if target is not None:
                        victim: Goblin | Elf = self[target]
                        victim.HP -= attacker.AP
                        if victim.HP <= 0:
                            # Target vanquished
                            if not elf_deaths_permitted and isinstance(victim, Elf):
                                raise ElfVanquished
                            # Remove vanquished target
                            self.combatants.remove(target)
                            # Vanquished targets disappear from the battlefield,
                            # mark their space as unoccupied.
                            self.mark_unoccupied(target)

                # Round complete
                completed_rounds += 1

        except BattleComplete:
            return completed_rounds * sum(self[c].HP for c in self.combatants)


class AOC2018Day15(AOC):
    """
    Day 15 of Advent of Code 2018
    """
    example_data: str = textwrap.dedent(
        """
        #######
        #.G...#
        #...EG#
        #.#.#G#
        #..G#E#
        #.....#
        #######
        """
    )

    validate_part1: str = 27730
    validate_part2: int = 4988

    def part1(self) -> int:
        """
        Return the outcome (product of number of rounds and total remaining
        Goblin HP).
        """
        battle_map = BattleMap(self.input)
        return battle_map.simulate()


    def part2(self) -> int:
        """
        Return the outcome for the smallest Elf attack power that results in a
        battle in which no Elfs are defeated.
        """
        battle_map = BattleMap(self.input)
        elf_attack: int
        for elf_attack in itertools.count(4):
            try:
                return battle_map.simulate(
                    elf_attack=elf_attack,
                    elf_deaths_permitted=False,
                )
            except ElfVanquished:
                continue

if __name__ == "__main__":
    aoc = AOC2018Day15()
    aoc.run()
