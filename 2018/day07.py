#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/7
'''
import itertools
import re
import string
import textwrap
from collections import defaultdict, deque

# Local imports
from aoc import AOC

# Type hints
Step = str
Requirements = dict[Step, set[Step]]


class AOC2018Day7(AOC):
    '''
    Day 7 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        Step C must be finished before step A can begin.
        Step C must be finished before step F can begin.
        Step A must be finished before step B can begin.
        Step A must be finished before step D can begin.
        Step B must be finished before step E can begin.
        Step D must be finished before step E can begin.
        Step F must be finished before step E can begin.
        '''
    )

    validate_part1: str = 'CABDFE'
    validate_part2: int = 15

    def load_requirements(self) -> Requirements:
        '''
        Load the requirements from the config file
        '''
        step_re: re.Pattern = re.compile(r'Step ([A-Z]).+step ([A-Z])')
        requirements: Requirements = defaultdict(set)

        for line in self.input.splitlines():
            required: Step
            step: Step
            required, step = step_re.match(line).groups()
            requirements[step].add(required)
            # Ensure that the dependent step also gets an entry in our
            # requirements dict
            requirements[required]  # pylint: disable=pointless-statement

        return requirements

    @staticmethod
    def remove_step(requirements: Requirements, step: Step) -> None:
        '''
        Remove the specified step from the requirements, and remove it as a
        dependency for any other steps where it is required.
        '''
        # Remove step
        del requirements[step]
        # Remove this step as a dependency from remaining steps
        deps: list[Step]
        for deps in requirements.values():
            deps.discard(step)

    def part1(self) -> str:
        '''
        Return the correct order in which to perform the steps from the
        instructions defined in the puzzle input
        '''
        requirements: Requirements = self.load_requirements()
        order: str = ''

        while requirements:
            for step in sorted(requirements):
                if not requirements[step]:
                    # This is the first alphabetical step which has no
                    # dependencies. Add it to the return string and remove from
                    # our requirements dict.
                    order += step
                    self.remove_step(requirements, step)
                    break

        return order

    def part2(self) -> int:
        '''
        Return the time it will take to complete all the steps
        '''
        workers: int = 2 if self.example else 5

        # Assuming A=1, B=2, ..., Z=26, the job will take that many seconds
        # plus an offset. For the example data that offset is 0 seconds, but
        # when run using the puzzle input this offset is an additional 60
        # seconds (i.e., A=61, B=62, ..., Z=86).
        offset: int = 0 if self.example else 60
        duration: dict[Step, int] = {
            letter: seconds + offset
            for letter, seconds in zip(
                string.ascii_uppercase,
                itertools.count(1)
            )
        }

        requirements: Requirements = self.load_requirements()

        jobs: dict[Step, int] = {}
        job_queue: deque[Step] = deque()

        time_elapsed: int
        for time_elapsed in itertools.count():

            # Tick one second off of each running job
            for step in list(jobs):
                jobs[step] -= 1
                if not jobs[step]:
                    # Clean up finished job
                    del jobs[step]
                    self.remove_step(requirements, step)

            # If no jobs remain, no steps remain, and there is nothing in the
            # job queue, then we are done. Return the elapsed time.
            if not any((jobs, requirements, job_queue)):
                return time_elapsed

            # Add any newly-available jobs to the queue
            job_queue.extend(
                step for step in sorted(requirements)
                if not requirements[step]
                and step not in job_queue
                and step not in jobs
            )

            # Assign jobs to available workers
            while job_queue and len(jobs) < workers:
                step: Step = job_queue.popleft()
                jobs[step] = duration[step]


if __name__ == '__main__':
    aoc = AOC2018Day7()
    aoc.run()
