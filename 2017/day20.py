#!/usr/bin/env python
'''
https://adventofcode.com/2017/day/20
'''
from __future__ import annotations
import itertools
import re
import textwrap
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass

# Local imports
from aoc import AOC, Coordinate3D

CENTER = Coordinate3D(0, 0, 0)


@dataclass
class ParticleMan:
    '''
    Doing the things a particle can
    '''
    id: int
    position: Coordinate3D
    velocity: Coordinate3D
    acceleration: Coordinate3D

    def update(self) -> None:
        '''
        Update the Particle's position and velocity
        '''
        self.velocity = self.velocity + self.acceleration
        self.position = self.position + self.velocity


class AOC2017Day20(AOC):
    '''
    Day 20 of Advent of Code 2017
    '''
    example_data_part1: str = textwrap.dedent(
        '''
        p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
        p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
        '''
    )

    example_data_part2: str = textwrap.dedent(
        '''
        p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
        p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
        p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
        p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
        '''
    )

    validate_part1: int = 0
    validate_part2: int = 1

    def load_particles(self, data: str) -> list[ParticleMan]:
        '''
        Load the input data
        '''
        def parse_line(line: str) -> Iterator[Coordinate3D]:
            '''
            Gather the integer values and generate Coordinate3D objects for
            each set of 3 of them.
            '''
            numbers: list[int] = [int(n) for n in re.findall(r'-?\d+', line)]
            index: int = 0
            size: int = 3
            xyz: list[int]
            while (xyz := numbers[index:index + size]):
                yield Coordinate3D(*xyz)
                index += size

        return [
            ParticleMan(index, *parse_line(line))
            for index, line in enumerate(data.splitlines())
        ]

    def part1(self) -> int:
        '''
        Return the ID of the particle that will "over the long run" remain
        closest to the center point.
        '''
        # As time approaches infinity, irrespective of the starting position
        # and velocity of a particle, the particle with the lowest acceleration
        # will end up being the closest to the center point. So instead of
        # simulating each movement for each particle until the position has
        # stablized, we can simply return the particle with the lowest
        # acceleration. This acceleration can be calculated as the Manhattan
        # Distance from the center point.
        return sorted(
            self.load_particles(self.input_part1),
            key=lambda p: p.acceleration.distance_from(CENTER),
        )[0].id

    def part2(self) -> int:
        '''
        Return the number of particles that will remain once there are no more
        collisions.
        '''
        Particles = list[ParticleMan]
        particles: Particles = self.load_particles(self.input_part2)
        num_particles: int = len(particles)
        streak: int = 1

        # Assume that 20 rounds with no change in group size means that all
        # collisions have taken place.
        while streak < 20:
            buckets: defaultdict[Coordinate3D, Particles] = defaultdict(list)
            for particle in particles:
                particle.update()
                buckets[particle.position.as_tuple].append(particle)

            particles = list(
                itertools.chain.from_iterable(
                    bucket for bucket in buckets.values()
                    if len(bucket) == 1
                )
            )

            if len(particles) == num_particles:
                streak += 1
            else:
                streak = 1
                num_particles = len(particles)

        return len(particles)


if __name__ == '__main__':
    aoc = AOC2017Day20()
    aoc.run()
