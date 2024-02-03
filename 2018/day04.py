#!/usr/bin/env python
'''
https://adventofcode.com/2018/day/4
'''
import itertools
import math
import re
import textwrap
from collections import Counter, defaultdict

# Local imports
from aoc import AOC


class AOC2018Day4(AOC):
    '''
    Day 4 of Advent of Code 2018
    '''
    example_data: str = textwrap.dedent(
        '''
        [1518-11-01 00:00] Guard #10 begins shift
        [1518-11-01 00:05] falls asleep
        [1518-11-01 00:25] wakes up
        [1518-11-01 00:30] falls asleep
        [1518-11-01 00:55] wakes up
        [1518-11-01 23:58] Guard #99 begins shift
        [1518-11-02 00:40] falls asleep
        [1518-11-02 00:50] wakes up
        [1518-11-03 00:05] Guard #10 begins shift
        [1518-11-03 00:24] falls asleep
        [1518-11-03 00:29] wakes up
        [1518-11-04 00:02] Guard #99 begins shift
        [1518-11-04 00:36] falls asleep
        [1518-11-04 00:46] wakes up
        [1518-11-05 00:03] Guard #99 begins shift
        [1518-11-05 00:45] falls asleep
        [1518-11-05 00:55] wakes up
        '''
    )

    validate_part1: int = 240
    validate_part2: int = 4455

    def post_init(self) -> None:
        '''
        Load input data
        '''
        self.guards: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.time_asleep: dict[int, int] = defaultdict(int)

        entry_re: re.Pattern = re.compile(r':(\d+)\] (.+)$')
        minute: str
        detail: str
        for minute, detail in (
            entry_re.search(line).groups()
            for line in sorted(self.input.splitlines())
        ):
            minute: int = int(minute)
            match detail.split():
                case ['Guard', guard_num, 'begins', 'shift']:
                    guard: int = int(guard_num[1:])
                case ['falls', 'asleep']:
                    asleep: int = minute
                case ['wakes', 'up']:
                    self.guards[guard].append((asleep, minute))
                    self.time_asleep[guard] += minute - asleep
                case _:
                    raise RuntimeError(f'Failed to process entry: {detail!r}')

    def sleepiest_minute(self, guard: int) -> tuple[int, int]:
        '''
        Return the minute the specified guard was most frequently asleep, along
        with the number of times the guard was asleep during that minute.
        '''
        return Counter(
            itertools.chain.from_iterable(
                (range(begin, end) for begin, end in self.guards[guard])
            )
        ).most_common(1)[0]

    def part1(self) -> int:
        '''
        Return the number of the sleepiest guard multiplied by the minute that
        guard was most frequently asleep
        '''
        guard: int = max(self.time_asleep.items(), key=lambda n: n[1])[0]
        return guard * self.sleepiest_minute(guard)[0]

    def part2(self) -> int:
        '''
        Return the minute where a guard was most frequently asleep, multiplied
        by the number of the guard who was asleep.
        '''
        # Below, a generator expression produces a series of tuples for each
        # guard, containing the guard number, the minute that guard was most
        # frequently asleep, and the number of times the guard was asleep
        # during that minute. Feed that into max(), sorting by the 3rd item
        # in the triple (i.e. the number of times the guard was asleep). The
        # result of the max() call is the tuple for that guard. From here we
        # just need to pass the first two items in that tuple to math.prod() to
        # get our answer.
        return math.prod(
            max(
                (
                    (guard,) + self.sleepiest_minute(guard)
                    for guard in self.guards
                ),
                key=lambda n: n[2]
            )[:2]
        )


if __name__ == '__main__':
    aoc = AOC2018Day4()
    aoc.run()
