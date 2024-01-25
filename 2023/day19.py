#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/19
'''
from __future__ import annotations
import math
import operator
import re
import textwrap
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

# Local imports
from aoc import AOC

# Type hints
Category = Literal['x', 'm', 'a', 's']
Bounds = dict[Category, 'Range']
ComparisonFunc = Callable[[int, int], bool]


@dataclass
class Range:
    '''
    Contains low/high values
    '''
    low: int = 1
    high: int = 4000

    @property
    def size(self) -> int:
        '''
        Return the size of the range
        '''
        return self.high - self.low + 1

    def copy(self) -> Range:
        '''
        Return a new Range object with the same parameters
        '''
        return Range(self.low, self.high)


@dataclass
class Part:
    '''
    Tracks ratings in each of the 4 rated categories
    '''
    x: int
    m: int
    a: int
    s: int
    workflows: dict[str, Workflow]

    def run_workflow(self, workflow: Workflow) -> str:
        '''
        Run a workflow on this Part
        '''
        for rule in self.workflows[workflow].rules:
            # Check for fallback rule at the end of the workflow
            if rule.condition is None or rule.condition.matches(self):
                return rule.result

        # Should never get here because all workflows should have a fallback
        raise RuntimeError(
            f'Unexpected error, workflow {workflow!r} has no fallback'
        )

    @property
    def accepted(self) -> bool:
        '''
        Run Part through workflows, returning True if the Part is accepted,
        otherwise False.
        '''
        workflow = 'in'
        while (workflow := self.run_workflow(workflow)) not in 'RA':
            pass
        return workflow == 'A'

    @property
    def rating(self) -> int:
        '''
        Return the overall rating for this Part
        '''
        return sum((self.x, self.m, self.a, self.s))


@dataclass
class Condition:
    '''
    Defines a condition and includes functions for comparison, as well as for
    getting the inverse of the condition during bounds filtering.
    '''
    category: Category
    operator: Literal['>', '<']
    value: int

    def __post_init__(self) -> None:
        '''
        Validation
        '''
        if self.category not in 'xmas':
            raise ValueError(f'Invalid category {self.category!r}')

        if self.operator not in ('><'):
            raise ValueError(f'Invalid operator {self.operator!r}')

        if not isinstance(self.value, int):
            raise TypeError('Value must be an integer')

    def matches(self, part: Part) -> bool:
        '''
        Returns True if the Part object matches the Condition's parameters
        '''
        match self.operator:
            case '>':
                opfunc: ComparisonFunc = operator.gt
            case '<':
                opfunc: ComparisonFunc = operator.lt

        return opfunc(getattr(part, self.category), self.value)

    @property
    def inverse(self) -> Condition:
        '''
        Return a Condition object representing the opposite comparison. We are
        assured of only integer values for this puzzle, so we can avoid needing
        to deal with >= or <= (and thus complicating the bounds filtering logic
        further... not that I would know that because I spent too long going
        down that path already...) by returning a Condition with the opposite
        operator and an offset value. For example, > 5 contains everything
        _higher_ than 5 (i.e. 6, 7, 8, etc.), while the inverse would be < 5+1
        (i.e. 5, 4, 3, etc.).
        '''
        oper: str
        value: int

        match self.operator:
            case '>':
                oper = '<'
                value = self.value + 1
            case '<':
                oper = '>'
                value = self.value - 1

        return Condition(self.category, oper, value)


@dataclass
class Rule:
    '''
    Ties together a Condition with a result
    '''
    result: str
    condition: Condition | None = None


class Workflow:
    '''
    Represents a single workflow
    '''
    def __init__(self, workflow_def: str) -> None:
        '''
        Load and parse the workflow def
        '''
        name: str
        rules: str
        try:
            name, rules = re.match(r'([a-z]+)\{(.+)\}', workflow_def).groups()
        except AttributeError as exc:
            raise ValueError(f'Invalid workflow def {workflow_def!r}') from exc

        self.name: str = name
        self.rules: tuple[Rule, ...] = tuple(
            self.parse_rule(rule) for rule in rules.split(',')
        )

    @staticmethod
    def parse_rule(rule_def: str) -> Rule:
        '''
        Parse a single rule from the comma-separated sequence in the rule
        definition, returning a Rule instance associating the rule's result
        with a Condition object representing the inequality expression (or no
        expression for fallback rules).
        '''
        match rule_def.split(':'):
            case [condition, result]:
                match re.split(r'(<|>)', condition):
                    case [
                        ('x' | 'm' | 'a' | 's') as category,
                        ('<' | '>') as oper,
                        value,
                    ]:
                        return Rule(
                            result=result,
                            condition=Condition(category, oper, int(value)),
                        )
                    case _:
                        raise ValueError(
                            f'Invalid rule definition {rule_def!r}'
                        )
            case [result]:
                return Rule(result=result)


class AOC2023Day19(AOC):
    '''
    Day 19 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}

        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        '''
    )

    validate_part1: int = 19114
    validate_part2: int = 167409079868000

    def post_init(self) -> None:
        '''
        Load the workflows from the puzzle input
        '''
        workflow_defs: str
        part_defs: str
        workflow_defs, part_defs = self.input.split('\n\n')

        self.workflows: dict[str, Workflow] = {}
        for line in workflow_defs.splitlines():
            workflow = Workflow(line)
            self.workflows[workflow.name] = workflow

        self.parts: tuple[Part, ...] = tuple(
            Part(int(x), int(m), int(a), int(s), self.workflows)
            for x, m, a, s in (
                re.search(r'x=(\d+),m=(\d+),a=(\d+),s=(\d+)', line).groups()
                for line in part_defs.splitlines()
            )
        )

    @staticmethod
    def filter_bounds(
        bounds: Bounds,
        condition: Condition,
    ) -> Bounds:
        '''
        Use the rule to narrow the bounds passed in, returning new bounds.
        '''
        # Make shallow copy of bounds dict
        new_bounds: Bounds = bounds.copy()
        # Replace the category's bounds with a new Range object, so that
        # updating its ranges does not modify the Range object from the
        # Bounds dict passed in.
        new_range: Range = bounds[condition.category].copy()
        new_bounds[condition.category] = new_range

        # Update Range object according to the specified Condition. Note that a
        # Range object defines an _inclusive_ low and high (i.e. the low and
        # high values are both considered part of the valid range). Also, note
        # that a Condition refers to an _exclusive_ comparison (i.e. greater or
        # less than). So, when updating a Range, we need to consider the values
        # that would be valid if the condition matches. For a greater-than
        # Condition, the valid values would not include the Condition's value,
        # they would start at the value + 1. Similarly, for a less-than
        # condition, the valid numbers would start at value - 1.
        match condition.operator:
            case '>':
                new_range.low = max(new_range.low, condition.value + 1)
            case '<':
                new_range.high = min(new_range.high, condition.value - 1)

        return new_bounds

    def bounds(
        self,
        workflow: str = 'in',
        bounds: Bounds | None = None,
    ) -> list[Bounds]:
        '''
        Recursively pass through each workflow, following each possible rule
        path, using the Conditions in each rule to narrow down the permissiable
        bounds for each category.

        Similar to 2023 Day 5, the result of this will be a list of bounds,
        representing the subranges that matched a given rule for a given
        workflow path.
        '''
        bounds: Bounds = bounds or {category: Range() for category in 'xmas'}

        ret = []
        for rule in self.workflows[workflow].rules:

            overlap: Bounds
            non_overlap: Bounds | None

            if rule.condition is not None:
                overlap = self.filter_bounds(bounds, rule.condition)
                non_overlap = self.filter_bounds(bounds, rule.condition.inverse)
            else:
                overlap = bounds
                non_overlap = None

            match rule.result:
                case 'A':
                    ret.append(overlap)
                case 'R':
                    # Do nothing
                    pass
                case _:
                    # The bounds that overlap with this rule state that matches
                    # get passed to another workflow. Recursively narrow down
                    # the ones that match this workflow with the ones that
                    # match the next one (and all subsequent paths).
                    ret.extend(
                        self.bounds(
                            workflow=rule.result,
                            bounds=overlap,
                        )
                    )

            if non_overlap:
                # For remaining rules, only consider the narrowed bounds
                bounds = non_overlap

        return ret

    def part1(self) -> int:
        '''
        Return the sum of the ratings (i.e. the sum of all 4 categories) for
        each accpeted part.
        '''
        return sum(part.rating for part in self.parts if part.accepted)

    def part2(self) -> int:
        '''
        Return the number of unique combinations of ratings that result in an
        accepted part.

        After self.bounds() finishes its recursion, it will return a list of
        Bounds dicts reflecting the different possible branching paths. Each of
        these dicts contains a Range object for each rating category. The total
        number of unique combinations for each of these dicts is the product of
        the size of all 4 ranges. Adding up each of these products gives us the
        total number of possibilities for every possible workflow path.
        '''
        return sum(
            math.prod(r.size for r in bounds.values())
            for bounds in self.bounds()
        )


if __name__ == '__main__':
    aoc = AOC2023Day19()
    aoc.run()
