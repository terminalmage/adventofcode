#!/usr/bin/env python
'''
https://adventofcode.com/2015/day/5

--- Day 5: Doesn't He Have Intern-Elves For This? ---

Santa needs help figuring out which strings in his text file are naughty or
nice.

A nice string is one with all of the following properties:

- It contains at least three vowels (aeiou only), like aei, xazegov, or
  aeiouaeiouaeiou.

- It contains at least one letter that appears twice in a row, like xx, abcdde
  (dd), or aabbccdd (aa, bb, cc, or dd).

- It does not contain the strings ab, cd, pq, or xy, even if they are part of
  one of the other requirements.

For example:

-    ugknbfddgicrmopn is nice because it has at least three vowels
     (u...i...o...), a double letter (...dd...), and none of the disallowed
     substrings.

-    aaa is nice because it has at least three vowels and a double letter, even
     though the letters used by different rules overlap.

-    jchzalrnumimnmhp is naughty because it has no double letter.

-    haegwjzuvuyypxyu is naughty because it contains the string xy.

-    dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?

--- Part Two ---

Realizing the error of his ways, Santa has switched to a better model of
determining whether a string is naughty or nice. None of the old rules apply,
as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

- It contains a pair of any two letters that appears at least twice in the
  string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like
  aaa (aa, but it overlaps).

- It contains at least one letter which repeats with exactly one letter between
  them, like xyx, abcdefeghi (efe), or even aaa.

For example:

- qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a
  letter that repeats with exactly one letter between them (zxz).

- xxyxx is nice because it has a pair that appears twice and a letter that
  repeats with one between, even though the letters used by each rule overlap.

- uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a
  single letter between them.

- ieodomkazucvgmuy is naughty because it has a repeating letter with one
  between (odo), but no pair that appears twice.

How many strings are nice under these new rules?
'''
import re

# Local imports
from aoc import AOC


class AOC2015Day5(AOC):
    '''
    Day 5 of Advent of Code 2015
    '''
    day = 5

    def __init__(self, example: bool = False) -> None:
        '''
        Load the strings
        '''
        super().__init__(example=example)
        self.strings = self.input.read_text().splitlines()

    def part1(self) -> int:
        '''
        Return the number of strings which are nice under Part 1's rules
        '''
        vowels_re = re.compile(r'[aeiou]')
        duplicate_re = re.compile(r'([a-z])\1')
        verboten_re = re.compile('ab|cd|pq|xy')
        return sum(
            1 for item in self.strings
            if len(vowels_re.findall(item)) > 2
                and bool(duplicate_re.search(item))
                and not bool(verboten_re.search(item))
        )

    def part2(self) -> int:
        '''
        Return the number of strings which are nice under Part 2's rules
        '''
        strings = (
            'qjhvhtzxzqqjkmpb',
            'xxyxx',
            'uurcxstgmygtbstg',
            'ieodomkazucvgmuy',
        ) if self.example else self.strings

        repeat_re = re.compile(r'([a-z]{2}).*\1')
        sandwich_re = re.compile(r'([a-z])[a-z]\1')
        return sum(
            1 for item in strings
            if bool(repeat_re.search(item)) and bool(sandwich_re.search(item))
        )


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2015Day5(example=True)
    aoc.validate(aoc.part1(), 2)
    aoc.validate(aoc.part2(), 2)
    # Run against actual data
    aoc = AOC2015Day5(example=False)
    aoc.run()
