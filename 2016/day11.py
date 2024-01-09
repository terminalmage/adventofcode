#!/usr/bin/env python
'''
https://adventofcode.com/2016/day/11
'''
import itertools
import heapq
from typing import Literal

# Local imports
from aoc import AOC

# Positive values will refer to microchips of a given element, while the
# negative counterpart will be a generator for that element.
HYDROGEN = 1
LITHIUM = 2
PROMETHIUM = 3
COBALT = 4
CURIUM = 5
RUTHENIUM = 6
PLUTONIUM = 7
ELERIUM = 8
DILITHIUM = 9

BOTTOM_FLOOR = 0
TOP_FLOOR = 3

# Tuple of ints representing contents of a given floor. Note that to make this
# work properly with heapq, we must have reliably-ordered values, so this tuple
# of ints must be sorted.
Floor = frozenset[int]
# Collection of all four floors
Floors = tuple[Floor, Floor, Floor, Floor]
# Index of floor where elevator is currently located (0-3)
Elevator = Literal[0, 1, 2, 3]
# Current state is represented by the current position of the elevator, along
# with the state of each floor
State = tuple[Elevator, Floors]


class AOC2016Day11(AOC):
    '''
    Day 11 of Advent of Code 2016
    '''
    day = 11

    def __init__(self, example: bool = False) -> None:
        '''
        Hard-code the initial state since the puzzle input is not in a
        parseable format.
        '''
        super().__init__(example=example)
        elevator: Elevator = 0
        if self.example:
            self.initial_state = (
                elevator, (
                    self.floor(HYDROGEN, LITHIUM),
                    self.floor(-HYDROGEN),
                    self.floor(-LITHIUM),
                    self.floor(),
                )
            )
        else:
            self.initial_state = (
                elevator, (
                    self.floor(-PROMETHIUM, PROMETHIUM),
                    self.floor(-COBALT, -CURIUM, -RUTHENIUM, -PLUTONIUM),
                    self.floor(COBALT, CURIUM, RUTHENIUM, PLUTONIUM),
                    self.floor(),
                )
            )

    @staticmethod
    def floor(*contents: int) -> Floor:
        '''
        Given a sequence of ints passed in as positional parameters, return
        them as a frozenset.
        '''
        return frozenset(contents)

    @staticmethod
    def empty(floor: Floor) -> bool:
        '''
        Return True if floor is empty, otherwise False
        '''
        return not floor

    @staticmethod
    def valid(*floors: Floor) -> bool:
        '''
        Return True if all the floor configurations passed in are valid,
        otherwise False
        '''
        for floor in floors:
            if not floor or min(floor) > 0:
                # Floor is empty or contains only microchips (generators are
                # represented by negative numbers).
                continue
            # Get all the chips on this floor (chips are represented by
            # positive numbers).
            chips: Floor = frozenset(item for item in floor if item > 0)
            # If any of the chips are not accompanied by their companion
            # generator, then this is an invalid configuration.
            if any(-chip not in floor for chip in chips):
                return False

        # No invalid configurations found in any of the specified floor
        # configurations, so return True
        return True

    def best(self, initial_state: State) -> int:
        '''
        Calculate the lowest number of steps to move all components from their
        initial positions to the top floor.
        '''
        visited: dict[State, int] = {}
        states: list[tuple[int, State]] = [(0, initial_state)]

        while states:
            # Get the next move from the queue
            state: State = heapq.heappop(states)[1]

            # Unpack the state
            elevator: Elevator
            floors: Floors
            elevator, floors = state

            # Check to see if we've reached the exit condition (i.e. all floors
            # but the top floor are empty). As this is a BFS, the first time we
            # reach the exit condition will be the cheapest, in terms of steps.
            if elevator == TOP_FLOOR and all(
                self.empty(floor) for floor in floors[:TOP_FLOOR]
            ):
                return visited[state]

            # We can move either one or two components from the current floor
            # at a time.
            for to_move in itertools.chain.from_iterable((
                itertools.combinations(floors[elevator], 2),
                itertools.combinations(floors[elevator], 1),
            )):
                for delta in (-1, 1):
                    new_elevator: Elevator = elevator + delta

                    # Skip invalid floor numbers
                    if not BOTTOM_FLOOR <= new_elevator <= TOP_FLOOR:
                        continue

                    # Don't attempt to move anything down if there's nothing
                    # below your current floor, that's just wasted movement.
                    if delta == -1 and not any(
                        floor for floor in floors[new_elevator::-1]
                    ):
                        continue

                    # Since we're making changes to the floors, convert them to
                    # a list temporarily
                    new_floors: list[Floor] = list(floors)
                    # Remove the components we're moving from the current floor
                    new_floors[elevator] = self.floor(
                        *(
                            component for component in new_floors[elevator]
                            if component not in to_move
                        )
                    )
                    new_floors[new_elevator] = new_floors[new_elevator] | set(to_move)
                    # Don't proceed if modifications made to current and new
                    # floor number result in invalid states
                    if not self.valid(
                        new_floors[elevator],
                        new_floors[new_elevator],
                    ):
                        continue

                    new_state: State = (new_elevator, tuple(new_floors))
                    new_steps: int = visited.get(state, 0) + 1

                    # Only add this potential new configuration to the queue if
                    # either A) it has not yet been tried, or B) it has been
                    # tried but at a worse (i.e. higher) step count.
                    if (
                        new_state not in visited
                        or new_steps < visited[new_state]
                    ):
                        visited[new_state] = new_steps
                        # Pushing onto a list using heapq.heappush will add it
                        # in sorted order, while popping removes the item which
                        # sorts as the lowest. Thus, we will push a combination
                        # of an integer "priority" value along with the new
                        # floor configurations. This priority value is
                        # calculated as the current step count minus the number
                        # of items on the top floor. In this way, lower step
                        # counts will be prioritized over higher step counts,
                        # and for identical step counts, configurations closer
                        # to the goal configuration will take precedence.
                        #
                        # NOTE: My initial solution just used new_steps minus
                        # the number of items on the top floor. Added a *10
                        # multiplier after seeing a similar solution by
                        # /u/adrian17, which speeds up Part 2 by 70%.
                        heapq.heappush(
                            states, (
                                new_steps - len(new_floors[TOP_FLOOR]) * 10,
                                new_state
                            )
                        )


    def part1(self) -> int:
        '''
        Calculate the minimum steps to bring all components to the top floor
        '''
        return self.best(initial_state=self.initial_state)

    def part2(self) -> int:
        '''
        Calculate the minimum steps to bring all components to the top floor
        using the additional components added for Part 2
        '''
        elevator: Elevator
        floors: Floors
        elevator, floors = self.initial_state
        new_floors: list[Floor] = list(floors)
        # Add the new components to the bottom floor
        new_floors[BOTTOM_FLOOR] = self.floor(
            ELERIUM, DILITHIUM, -ELERIUM, -DILITHIUM, *new_floors[BOTTOM_FLOOR]
        )
        initial_state: State = (elevator, tuple(new_floors))

        return self.best(initial_state=initial_state)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2016Day11(example=True)
    aoc.validate(aoc.part1(), 11)
    # Run against actual data
    aoc = AOC2016Day11(example=False)
    aoc.run()
