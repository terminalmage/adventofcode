#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/19
'''
import functools
import math
import re
from collections.abc import Iterator

# Local imports
from aoc import AOC


class Blueprint:
    '''
    Represents a single blueprint
    '''
    def __init__(
        self,
        blueprint_id: int,
        ore_cost: int,
        clay_cost: int,
        obsidian_cost: tuple[int, int],
        geode_cost: tuple[int, int],
    ) -> None:
        '''
        Initialize the object
        '''
        self.blueprint_id: int = blueprint_id
        self.ore_cost: int = ore_cost
        self.clay_cost: int = clay_cost
        # tuple of ore and clay cost
        self.obsidian_cost: tuple[int, int] = obsidian_cost
        # tuple of ore and obsidian cost
        self.geode_cost: tuple[int, int] = geode_cost

        # Initialize the attributes for the simulated number of minutes, and
        # the max number of geodes that can be produced in the simulated time
        self.minutes: int = 0
        self.max_geodes: int = 0

        # Don't make more ore robots than we need to generate enough ore to
        # build any kind of robot
        self.ore_robot_threshold: int = max(
            self.ore_cost,
            self.clay_cost,
            self.obsidian_cost[0],
            self.geode_cost[0],
        )

    @property
    def quality_level(self) -> int:
        '''
        The quality level is the max number of geodes the blueprint can produce
        in the simulated time, multiplied by the blueprint ID
        '''
        return self.blueprint_id * self.max_geodes

    @property
    def robot_types(self) -> Iterator[str]:
        '''
        Generator to return the robot types
        '''
        yield 'ore'
        yield 'clay'
        yield 'obsidian'
        yield 'geode'

    @functools.lru_cache
    def max_additional(self, minutes: int) -> int:
        '''
        The max additional geodes that can be produced in the remaining time
        (i.e. minutes - 1). This is a best-case scenario, assuming that you
        have enough resources to build a geode robot in every remaining turn.
        '''
        return ((minutes - 1) * minutes) // 2

    def simulate(self, minutes: int) -> int:
        '''
        Simulate the blueprint over the specified number of minutes

        Returns the max number of geodes that can be produce, and also sets
        this instance's "minutes" and "max_geodes" attributes.
        '''
        # Set the minutes attribute and reset max_geodes
        self.minutes: int = minutes
        self.max_geodes: int = 0

        def _simulate(
            minutes: int,
            robot_type: str,
            ore_robots: int = 1,
            clay_robots: int = 0,
            obsidian_robots: int = 0,
            geode_robots: int = 0,
            ore_stock: int = 0,
            clay_stock: int = 0,
            obsidian_stock: int = 0,
            geode_stock: int = 0,
        ) -> int:
            '''
            Depth-first search algorithm to determine the most geodes that can
            be produced in the specified time.

            Time-saving logic inspired by /u/Boojum in
            https://old.reddit.com/r/adventofcode/comments/zpihwi/2022_day_19_solutions/j0tls7a/
            '''
            match robot_type:
                case 'ore':
                    # Don't build more ore robots if we have enough of them to
                    # make enough ore in a single minute to build any of the
                    # other robot types
                    if ore_robots >= self.ore_robot_threshold:
                        return
                case 'clay':
                    # Don't build more clay robots if we have enough of them to
                    # generate enough clay in a single minute to build an
                    # obsidian robot
                    if clay_robots >= self.obsidian_cost[1]:
                        return
                case 'obsidian':
                    # Don't build more obsidian robots if we literally cant
                    # (because we have no clay robots yet) or if we already
                    # have enough obsidian to build a geode robot
                    if not clay_robots or obsidian_stock >= self.geode_cost[1]:
                        return
                case 'geode':
                    # Don't try to build a geode robot if we literally can't
                    # (because we have no obsidian robots yet)
                    if not obsidian_robots:
                        return
                case '_':
                    raise ValueError(f'Invalid robot_type {robot_type!r}')

            if (
                geode_stock
                + (geode_robots * minutes)
                + self.max_additional(minutes)
            ) <= self.max_geodes:
                # If the max amount of possible geodes we could produce in this
                # branch of the algorithm is not greater than the current
                # maximum, there is no point in continuing, as this branch
                # could never catch up.
                return

            for time_remaining in range(minutes, 0, -1):
                match robot_type:
                    case 'ore':
                        if ore_stock >= self.ore_cost:
                            for next_robot_type in self.robot_types:
                                # Simulate all possible remaining rounds
                                # assuming that at this point in the simulation
                                # we added one ore robot
                                _simulate(
                                    time_remaining - 1,
                                    next_robot_type,
                                    ore_robots + 1,
                                    clay_robots,
                                    obsidian_robots,
                                    geode_robots,
                                    # Update mineral stocks. Add one unit of
                                    # each mineral for each robot of that type,
                                    # and subtract resources spent this round.
                                    ore_stock - self.ore_cost + ore_robots,
                                    clay_stock + clay_robots,
                                    obsidian_stock + obsidian_robots,
                                    geode_stock + geode_robots,
                                )
                            return

                    case 'clay':
                        if ore_stock >= self.clay_cost:
                            for next_robot_type in self.robot_types:
                                # Simulate all possible remaining rounds
                                # assuming that at this point in the simulation
                                # we added one clay robot
                                _simulate(
                                    time_remaining - 1,
                                    next_robot_type,
                                    ore_robots,
                                    clay_robots + 1,
                                    obsidian_robots,
                                    geode_robots,
                                    # Update mineral stocks. Add one unit of
                                    # each mineral for each robot of that type,
                                    # and subtract resources spent this round.
                                    ore_stock + ore_robots - self.clay_cost,
                                    clay_stock + clay_robots,
                                    obsidian_stock + obsidian_robots,
                                    geode_stock + geode_robots,
                                )
                            return

                    case 'obsidian':
                        if (
                            ore_stock >= self.obsidian_cost[0] and
                            clay_stock >= self.obsidian_cost[1]
                        ):
                            for next_robot_type in self.robot_types:
                                # Simulate all possible remaining rounds
                                # assuming that at this point in the simulation
                                # we added one obsidian robot
                                _simulate(
                                    time_remaining - 1,
                                    next_robot_type,
                                    ore_robots,
                                    clay_robots,
                                    obsidian_robots + 1,
                                    geode_robots,
                                    # Update mineral stocks. Add one unit of
                                    # each mineral for each robot of that type,
                                    # and subtract resources spent this round.
                                    ore_stock + ore_robots - self.obsidian_cost[0],
                                    clay_stock + clay_robots - self.obsidian_cost[1],
                                    obsidian_stock + obsidian_robots,
                                    geode_stock + geode_robots,
                                )
                            return

                    case 'geode':
                        if (
                            ore_stock >= self.geode_cost[0] and
                            obsidian_stock >= self.geode_cost[1]
                        ):
                            for next_robot_type in self.robot_types:
                                # Simulate all possible remaining rounds
                                # assuming that at this point in the simulation
                                # we added one geode robot
                                _simulate(
                                    time_remaining - 1,
                                    next_robot_type,
                                    ore_robots,
                                    clay_robots,
                                    obsidian_robots,
                                    geode_robots + 1,
                                    # Update mineral stocks. Add one unit of
                                    # each mineral for each robot of that type,
                                    # and subtract resources spent this round.
                                    ore_stock + ore_robots - self.geode_cost[0],
                                    clay_stock + clay_robots,
                                    obsidian_stock + obsidian_robots - self.geode_cost[1],
                                    geode_stock + geode_robots,
                                )
                            return

                # Update mineral stocks. Add one unit of each mineral for each
                # robot of that type. Note that we also incremented above in
                # the match/case block, but that was being done to kick off new
                # branches of the simulation, so we need to repeat that here
                # for the current round.A
                ore_stock += ore_robots
                clay_stock += clay_robots
                obsidian_stock += obsidian_robots
                geode_stock += geode_robots

            # Update the max_geodes if this branch produced a higher amount
            self.max_geodes = max(self.max_geodes, geode_stock)

            ### End of _simulate closure

        robot_type: str
        for robot_type in self.robot_types:
            _simulate(minutes, robot_type)

        return self.max_geodes


class AOC2022Day19(AOC):
    '''
    Day 19 of Advent of Code 2022
    '''
    def load_blueprints(self) -> list[Blueprint]:
        '''
        Return a list of Blueprint objects as loaded from the input file
        '''
        return [
            Blueprint(
                blueprint_id=values[0],
                ore_cost=values[1],
                clay_cost=values[2],
                obsidian_cost=values[3:5],
                geode_cost=values[5:7],
            )
            for values in (
                tuple(map(int, re.findall(r'\d+', line)))
                for line in self.input.splitlines()
            )
        ]

    def part1(self) -> int:
        '''
        Calculate the sum of the quality levels for each of the blueprints
        '''
        # Run the simulation on all blueprints
        blueprints: list[Blueprint] = self.load_blueprints()
        blueprint: Blueprint
        for blueprint in blueprints:
            blueprint.simulate(minutes=24)
        # Return the sum of all the quality levels
        return sum(blueprint.quality_level for blueprint in blueprints)

    def part2(self) -> int:
        '''
        Calculate the product of the maximum number of geodes that can be
        produced for each of the first three blueprints in the list
        '''
        blueprints: list[Blueprint] = self.load_blueprints()[:3]
        blueprint: Blueprint
        for blueprint in blueprints:
            blueprint.simulate(minutes=32)
        # Return the product of the max_geodes that can be produced by the
        # first three blueprints
        return math.prod((blueprint.max_geodes for blueprint in blueprints))


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day19(example=True)
    aoc.validate(aoc.part1(), 33)
    aoc.validate(aoc.part2(), 3472)
    # Run against actual data
    aoc = AOC2022Day19(example=False)
    aoc.run()
