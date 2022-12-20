#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/19

--- Day 19: Not Enough Minerals ---

Your scans show that the lava did indeed form obsidian!

The wind has changed direction enough to stop sending lava droplets toward you,
so you and the elephants exit the cave. As you do, you notice a collection of
geodes around the pond. Perhaps you could use the obsidian to create some
geode-cracking robots and break them open?

To collect the obsidian from the bottom of the pond, you'll need waterproof
obsidian-collecting robots. Fortunately, there is an abundant amount of clay
nearby that you can use to make them waterproof.

In order to harvest the clay, you'll need special-purpose clay-collecting
robots. To make any type of robot, you'll need ore, which is also plentiful but
in the opposite direction from the clay.

Collecting ore requires ore-collecting robots with big drills. Fortunately, you
have exactly one ore-collecting robot in your pack that you can use to
kickstart the whole operation.

Each robot can collect 1 of its resource type per minute. It also takes one
minute for the robot factory (also conveniently from your pack) to construct
any type of robot, although it consumes the necessary resources available when
construction begins.

The robot factory has many blueprints (your puzzle input) you can choose from,
but once you've configured it with a blueprint, you can't change it. You'll
need to work out which blueprint is best.

For example:

Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.

(Blueprints have been line-wrapped here for legibility. The robot factory's
actual assortment of blueprints are provided one blueprint per line.)

The elephants are starting to look hungry, so you shouldn't take too long; you
need to figure out which blueprint would maximize the number of opened geodes
after 24 minutes by figuring out which robots to build and when to build them.

Using blueprint 1 in the example above, the largest number of geodes you could
open in 24 minutes is 9. One way to achieve that is:

== Minute 1 ==
1 ore-collecting robot collects 1 ore; you now have 1 ore.

== Minute 2 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.

== Minute 3 ==
Spend 2 ore to start building a clay-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
The new clay-collecting robot is ready; you now have 1 of them.

== Minute 4 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
1 clay-collecting robot collects 1 clay; you now have 1 clay.

== Minute 5 ==
Spend 2 ore to start building a clay-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
1 clay-collecting robot collects 1 clay; you now have 2 clay.
The new clay-collecting robot is ready; you now have 2 of them.

== Minute 6 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
2 clay-collecting robots collect 2 clay; you now have 4 clay.

== Minute 7 ==
Spend 2 ore to start building a clay-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
2 clay-collecting robots collect 2 clay; you now have 6 clay.
The new clay-collecting robot is ready; you now have 3 of them.

== Minute 8 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
3 clay-collecting robots collect 3 clay; you now have 9 clay.

== Minute 9 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.
3 clay-collecting robots collect 3 clay; you now have 12 clay.

== Minute 10 ==
1 ore-collecting robot collects 1 ore; you now have 4 ore.
3 clay-collecting robots collect 3 clay; you now have 15 clay.

== Minute 11 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 2 ore.
3 clay-collecting robots collect 3 clay; you now have 4 clay.
The new obsidian-collecting robot is ready; you now have 1 of them.

== Minute 12 ==
Spend 2 ore to start building a clay-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
3 clay-collecting robots collect 3 clay; you now have 7 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 1 obsidian.
The new clay-collecting robot is ready; you now have 4 of them.

== Minute 13 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
4 clay-collecting robots collect 4 clay; you now have 11 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 2 obsidian.

== Minute 14 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 15 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 3 obsidian.

== Minute 15 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
4 clay-collecting robots collect 4 clay; you now have 5 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 4 obsidian.
The new obsidian-collecting robot is ready; you now have 2 of them.

== Minute 16 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.
4 clay-collecting robots collect 4 clay; you now have 9 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 6 obsidian.

== Minute 17 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 13 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 8 obsidian.

== Minute 18 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
1 ore-collecting robot collects 1 ore; you now have 2 ore.
4 clay-collecting robots collect 4 clay; you now have 17 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 3 obsidian.
The new geode-cracking robot is ready; you now have 1 of them.

== Minute 19 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 21 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 5 obsidian.
1 geode-cracking robot cracks 1 geode; you now have 1 open geode.

== Minute 20 ==
1 ore-collecting robot collects 1 ore; you now have 4 ore.
4 clay-collecting robots collect 4 clay; you now have 25 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 7 obsidian.
1 geode-cracking robot cracks 1 geode; you now have 2 open geodes.

== Minute 21 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
1 ore-collecting robot collects 1 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 29 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 2 obsidian.
1 geode-cracking robot cracks 1 geode; you now have 3 open geodes.
The new geode-cracking robot is ready; you now have 2 of them.

== Minute 22 ==
1 ore-collecting robot collects 1 ore; you now have 4 ore.
4 clay-collecting robots collect 4 clay; you now have 33 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 4 obsidian.
2 geode-cracking robots crack 2 geodes; you now have 5 open geodes.

== Minute 23 ==
1 ore-collecting robot collects 1 ore; you now have 5 ore.
4 clay-collecting robots collect 4 clay; you now have 37 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 6 obsidian.
2 geode-cracking robots crack 2 geodes; you now have 7 open geodes.

== Minute 24 ==
1 ore-collecting robot collects 1 ore; you now have 6 ore.
4 clay-collecting robots collect 4 clay; you now have 41 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 8 obsidian.
2 geode-cracking robots crack 2 geodes; you now have 9 open geodes.

However, by using blueprint 2 in the example above, you could do even better:
the largest number of geodes you could open in 24 minutes is 12.

Determine the quality level of each blueprint by multiplying that blueprint's
ID number with the largest number of geodes that can be opened in 24 minutes
using that blueprint. In this example, the first blueprint has ID 1 and can
open 9 geodes, so its quality level is 9. The second blueprint has ID 2 and can
open 12 geodes, so its quality level is 24. Finally, if you add up the quality
levels of all of the blueprints in the list, you get 33.

Determine the quality level of each blueprint using the largest number of
geodes it could produce in 24 minutes. What do you get if you add up the
quality level of all of the blueprints in your list?

--- Part Two ---

While you were choosing the best blueprint, the elephants found some food on
their own, so you're not in as much of a hurry; you figure you probably have 32
minutes before the wind changes direction again and you'll need to get out of
range of the erupting volcano.

Unfortunately, one of the elephants ate most of your blueprint list! Now, only
the first three blueprints in your list are intact.

In 32 minutes, the largest number of geodes blueprint 1 (from the example
above) can open is 56. One way to achieve that is:

== Minute 1 ==
1 ore-collecting robot collects 1 ore; you now have 1 ore.

== Minute 2 ==
1 ore-collecting robot collects 1 ore; you now have 2 ore.

== Minute 3 ==
1 ore-collecting robot collects 1 ore; you now have 3 ore.

== Minute 4 ==
1 ore-collecting robot collects 1 ore; you now have 4 ore.

== Minute 5 ==
Spend 4 ore to start building an ore-collecting robot.
1 ore-collecting robot collects 1 ore; you now have 1 ore.
The new ore-collecting robot is ready; you now have 2 of them.

== Minute 6 ==
2 ore-collecting robots collect 2 ore; you now have 3 ore.

== Minute 7 ==
Spend 2 ore to start building a clay-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
The new clay-collecting robot is ready; you now have 1 of them.

== Minute 8 ==
Spend 2 ore to start building a clay-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
1 clay-collecting robot collects 1 clay; you now have 1 clay.
The new clay-collecting robot is ready; you now have 2 of them.

== Minute 9 ==
Spend 2 ore to start building a clay-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
2 clay-collecting robots collect 2 clay; you now have 3 clay.
The new clay-collecting robot is ready; you now have 3 of them.

== Minute 10 ==
Spend 2 ore to start building a clay-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
3 clay-collecting robots collect 3 clay; you now have 6 clay.
The new clay-collecting robot is ready; you now have 4 of them.

== Minute 11 ==
Spend 2 ore to start building a clay-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
4 clay-collecting robots collect 4 clay; you now have 10 clay.
The new clay-collecting robot is ready; you now have 5 of them.

== Minute 12 ==
Spend 2 ore to start building a clay-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
5 clay-collecting robots collect 5 clay; you now have 15 clay.
The new clay-collecting robot is ready; you now have 6 of them.

== Minute 13 ==
Spend 2 ore to start building a clay-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
6 clay-collecting robots collect 6 clay; you now have 21 clay.
The new clay-collecting robot is ready; you now have 7 of them.

== Minute 14 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 2 ore.
7 clay-collecting robots collect 7 clay; you now have 14 clay.
The new obsidian-collecting robot is ready; you now have 1 of them.

== Minute 15 ==
2 ore-collecting robots collect 2 ore; you now have 4 ore.
7 clay-collecting robots collect 7 clay; you now have 21 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 1 obsidian.

== Minute 16 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
7 clay-collecting robots collect 7 clay; you now have 14 clay.
1 obsidian-collecting robot collects 1 obsidian; you now have 2 obsidian.
The new obsidian-collecting robot is ready; you now have 2 of them.

== Minute 17 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 2 ore.
7 clay-collecting robots collect 7 clay; you now have 7 clay.
2 obsidian-collecting robots collect 2 obsidian; you now have 4 obsidian.
The new obsidian-collecting robot is ready; you now have 3 of them.

== Minute 18 ==
2 ore-collecting robots collect 2 ore; you now have 4 ore.
7 clay-collecting robots collect 7 clay; you now have 14 clay.
3 obsidian-collecting robots collect 3 obsidian; you now have 7 obsidian.

== Minute 19 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
7 clay-collecting robots collect 7 clay; you now have 7 clay.
3 obsidian-collecting robots collect 3 obsidian; you now have 10 obsidian.
The new obsidian-collecting robot is ready; you now have 4 of them.

== Minute 20 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 3 ore.
7 clay-collecting robots collect 7 clay; you now have 14 clay.
4 obsidian-collecting robots collect 4 obsidian; you now have 7 obsidian.
The new geode-cracking robot is ready; you now have 1 of them.

== Minute 21 ==
Spend 3 ore and 14 clay to start building an obsidian-collecting robot.
2 ore-collecting robots collect 2 ore; you now have 2 ore.
7 clay-collecting robots collect 7 clay; you now have 7 clay.
4 obsidian-collecting robots collect 4 obsidian; you now have 11 obsidian.
1 geode-cracking robot cracks 1 geode; you now have 1 open geode.
The new obsidian-collecting robot is ready; you now have 5 of them.

== Minute 22 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 2 ore.
7 clay-collecting robots collect 7 clay; you now have 14 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 9 obsidian.
1 geode-cracking robot cracks 1 geode; you now have 2 open geodes.
The new geode-cracking robot is ready; you now have 2 of them.

== Minute 23 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 2 ore.
7 clay-collecting robots collect 7 clay; you now have 21 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 7 obsidian.
2 geode-cracking robots crack 2 geodes; you now have 4 open geodes.
The new geode-cracking robot is ready; you now have 3 of them.

== Minute 24 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 2 ore.
7 clay-collecting robots collect 7 clay; you now have 28 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 5 obsidian.
3 geode-cracking robots crack 3 geodes; you now have 7 open geodes.
The new geode-cracking robot is ready; you now have 4 of them.

== Minute 25 ==
2 ore-collecting robots collect 2 ore; you now have 4 ore.
7 clay-collecting robots collect 7 clay; you now have 35 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 10 obsidian.
4 geode-cracking robots crack 4 geodes; you now have 11 open geodes.

== Minute 26 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 4 ore.
7 clay-collecting robots collect 7 clay; you now have 42 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 8 obsidian.
4 geode-cracking robots crack 4 geodes; you now have 15 open geodes.
The new geode-cracking robot is ready; you now have 5 of them.

== Minute 27 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 4 ore.
7 clay-collecting robots collect 7 clay; you now have 49 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 6 obsidian.
5 geode-cracking robots crack 5 geodes; you now have 20 open geodes.
The new geode-cracking robot is ready; you now have 6 of them.

== Minute 28 ==
2 ore-collecting robots collect 2 ore; you now have 6 ore.
7 clay-collecting robots collect 7 clay; you now have 56 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 11 obsidian.
6 geode-cracking robots crack 6 geodes; you now have 26 open geodes.

== Minute 29 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 6 ore.
7 clay-collecting robots collect 7 clay; you now have 63 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 9 obsidian.
6 geode-cracking robots crack 6 geodes; you now have 32 open geodes.
The new geode-cracking robot is ready; you now have 7 of them.

== Minute 30 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 6 ore.
7 clay-collecting robots collect 7 clay; you now have 70 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 7 obsidian.
7 geode-cracking robots crack 7 geodes; you now have 39 open geodes.
The new geode-cracking robot is ready; you now have 8 of them.

== Minute 31 ==
Spend 2 ore and 7 obsidian to start building a geode-cracking robot.
2 ore-collecting robots collect 2 ore; you now have 6 ore.
7 clay-collecting robots collect 7 clay; you now have 77 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 5 obsidian.
8 geode-cracking robots crack 8 geodes; you now have 47 open geodes.
The new geode-cracking robot is ready; you now have 9 of them.

== Minute 32 ==
2 ore-collecting robots collect 2 ore; you now have 8 ore.
7 clay-collecting robots collect 7 clay; you now have 84 clay.
5 obsidian-collecting robots collect 5 obsidian; you now have 10 obsidian.
9 geode-cracking robots crack 9 geodes; you now have 56 open geodes.

However, blueprint 2 from the example above is still better; using it, the
largest number of geodes you could open in 32 minutes is 62.

You no longer have enough blueprints to worry about quality levels. Instead,
for each of the first three blueprints, determine the largest number of geodes
you could open; then, multiply these three values together.

Don't worry about quality levels; instead, just determine the largest number of
geodes you could open using each of the first three blueprints. What do you get
if you multiply these numbers together?
'''
import functools
import re
from collections.abc import Iterator

# Local imports
from aoc2022 import AOC2022


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
        self.blueprint_id = blueprint_id
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        # tuple of ore and clay cost
        self.obsidian_cost = obsidian_cost
        # tuple of ore and obsidian cost
        self.geode_cost = geode_cost

        # Initialize the attributes for the simulated number of minutes, and
        # the max number of geodes that can be produced in the simulated time
        self.minutes = self.max_geodes = 0

        # Don't make more ore robots than we need to generate enough ore to
        # build any kind of robot
        self.ore_robot_threshold = max(
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
        self.minutes = minutes
        self.max_geodes = 0

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

        for robot_type in self.robot_types:
            _simulate(minutes, robot_type)

        return self.max_geodes


class AOC2022Day19(AOC2022):
    '''
    Day 19 of Advent of Code 2022
    '''
    day = 19

    def load_blueprints(self) -> list[Blueprint]:
        '''
        Return a list of Blueprint objects as loaded from the input file
        '''
        with self.input.open() as fh:
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
                    for line in fh
                )
            ]

    def part1(self) -> int:
        '''
        Calculate the sum of the quality levels for each of the blueprints
        '''
        # Run the simulation on all blueprints
        blueprints = self.load_blueprints()
        for blueprint in blueprints:
            blueprint.simulate(minutes=24)
        # Return the sum of all the quality levels
        return sum(blueprint.quality_level for blueprint in blueprints)

    def part2(self) -> int:
        '''
        Calculate the product of the maximum number of geodes that can be
        produced for each of the first three blueprints in the list
        '''
        blueprints = self.load_blueprints()[:3]
        for blueprint in blueprints:
            blueprint.simulate(minutes=32)
        # Return the product of the max_geodes that can be produced by the
        # first three blueprints
        return functools.reduce(
            lambda x, y: x * y,
            (blueprint.max_geodes for blueprint in blueprints)
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day19(example=True)
    aoc.validate(aoc.part1(), 33)
    aoc.validate(aoc.part2(), 3472)
    # Run against actual data
    aoc = AOC2022Day19(example=False)
    aoc.run()
