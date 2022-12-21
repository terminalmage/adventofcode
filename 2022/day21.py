#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/21

--- Day 21: Monkey Math ---

The monkeys are back! You're worried they're going to try to steal your stuff
again, but it seems like they're just holding their ground and making various
monkey noises at you.

Eventually, one of the elephants realizes you don't speak monkey and comes over
to interpret. As it turns out, they overheard you talking about trying to find
the grove; they can show you a shortcut if you answer their riddle.

Each monkey is given a job: either to yell a specific number or to yell the
result of a math operation. All of the number-yelling monkeys know their number
from the start; however, the math operation monkeys need to wait for two other
monkeys to yell a number, and those two other monkeys might also be waiting on
other monkeys.

Your job is to work out the number the monkey named root will yell before the
monkeys figure it out themselves.

For example:

root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32

Each line contains the name of a monkey, a colon, and then the job of that
monkey:

- A lone number means the monkey's job is simply to yell that number.

- A job like aaaa + bbbb means the monkey waits for monkeys aaaa and bbbb to
  yell each of their numbers; the monkey then yells the sum of those two
  numbers.

- aaaa - bbbb means the monkey yells aaaa's number minus bbbb's number.

- Job aaaa * bbbb will yell aaaa's number multiplied by bbbb's number.

- Job aaaa / bbbb will yell aaaa's number divided by bbbb's number.

So, in the above example, monkey drzm has to wait for monkeys hmdt and zczc to
yell their numbers. Fortunately, both hmdt and zczc have jobs that involve
simply yelling a single number, so they do this immediately: 32 and 2. Monkey
drzm can then yell its number by finding 32 minus 2: 30.

Then, monkey sjmn has one of its numbers (30, from monkey drzm), and already
has its other number, 5, from dbpl. This allows it to yell its own number by
finding 30 multiplied by 5: 150.

This process continues until root yells a number: 152.

However, your actual situation involves considerably more monkeys. What number
will the monkey named root yell?

--- Part Two ---

Due to some kind of monkey-elephant-human mistranslation, you seem to have
misunderstood a few key details about the riddle.

First, you got the wrong job for the monkey named root; specifically, you got
the wrong math operation. The correct operation for monkey root should be =,
which means that it still listens for two numbers (from the same two monkeys as
before), but now checks that the two numbers match.

Second, you got the wrong monkey for the job starting with humn:. It isn't a
monkey - it's you. Actually, you got the job wrong, too: you need to figure out
what number you need to yell so that root's equality check passes. (The number
that appears after humn: in your input is now irrelevant.)

In the above example, the number you need to yell to pass root's equality test
is 301. (This causes root to get the same number, 150, from both of its
monkeys.)

What number do you yell to pass root's equality test?
'''
import re
import sys

# Local imports
from aoc2022 import AOC2022

# Typing shortcuts
Expression = tuple[str, str, str]


class AOC2022Day21(AOC2022):
    '''
    Day 21 of Advent of Code 2022
    '''
    day = 21

    def __init__(self, example: bool = False) -> None:
        '''
        Load the monkeys into a data structure. If the monkey has an integer
        value associated with it, store that value. Otherwise, store a lambda
        that can be used to compute its value at a later time.
        '''
        super().__init__(example=example)

        monkey_re = re.compile(
            r'([a-z]+): (?:(\d+)|([a-z]+) ([*/+-]) ([a-z]+))'
        )

        self.monkeys = {}
        with self.input.open() as fh:
            for line in fh:
                name, value, lvalue, operand, rvalue = monkey_re.match(line).groups()
                if value is not None:
                    self.monkeys[name] = int(value)
                else:
                    self.monkeys[name] = (lvalue, operand, rvalue)

    def evaluate(
        self,
        name: str,
        monkeys: dict[str, int | Expression] | None = None,
        human: int | None = None,
    ) -> int:
        '''
        Calculate the value for the specified monkey
        '''
        if monkeys is None:
            monkeys = self.monkeys.copy()
        if human is not None:
            monkeys['humn'] = human

        value = monkeys[name]
        try:
            # Retrieve the lvalue and rvalue for the arithmetic expression,
            # computing those values if needed
            lvalue = self.evaluate(value[0], monkeys=monkeys)
            rvalue = self.evaluate(value[2], monkeys=monkeys)
            # Evaluate the arithmetic expression and replace the monkey's value
            # with the evaluated result
            monkeys[name] = eval(f'{lvalue} {value[1]} {rvalue}', {}, {})  # pylint: disable=eval-used
            # Return the evaluated result
            return monkeys[name]
        except TypeError:
            # The monkey already has an integer value assigned to it
            return value

    @staticmethod
    def normalize(value: int) -> int:
        '''
        If the value is an int, return an integer type
        '''
        int_value = int(value)
        if value == int_value:
            return int_value
        return value

    def part1(self) -> int | float:
        '''
        Decrypt the cipher and return the coordinates
        '''
        return self.normalize(self.evaluate('root'))

    def part2(self) -> int | float:
        '''
        Figure out the correct value to use for the "humn" variable, to make
        the two components of the root monkey's equation equal
        '''
        left, right = self.monkeys['root'][0], self.monkeys['root'][2]

        def _get_diff(human: int) -> int:
            '''
            Calculate both left and right monkeys with the specified value for
            the "humn" variable, and return the difference
            '''
            monkeys = self.monkeys.copy()
            lvalue = self.evaluate(left, monkeys=monkeys, human=human)
            rvalue = self.evaluate(right, monkeys=monkeys, human=human)
            return lvalue - rvalue

        modifier = _get_diff(1) > 0

        low = 0
        high = sys.maxsize

        while True:
            # Select the midpoint between low and high
            human = (low + high) // 2

            # Evaluate both lvalue and rvalue using this value for "humn"
            diff = _get_diff(human)

            if not diff:
                # Both lvalue and rvalue were identical, break out of loop
                break

            if human == low:
                # No match found
                raise RuntimeError('Binary search failed')

            if diff > 0:
                if modifier:
                    low = human
                else:
                    high = human
            else:
                if modifier:
                    high = human
                else:
                    low = human

        return self.normalize(human)


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day21(example=True)
    aoc.validate(aoc.part1(), 152)
    aoc.validate(aoc.part2(), 301)
    # Run against actual data
    aoc = AOC2022Day21(example=False)
    aoc.run()
