'''
Base class for Advent of Code submissions
'''
from __future__ import annotations
import copy
import functools
import hashlib
import math
import operator
import re
import sys
import time
from collections import namedtuple, Counter
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Type hints
Row = float
Column = float
XY = tuple[Row, Column]
XYZ = tuple[float, float, float]
Directions = tuple[XY, XY, XY, XY]

# NOTE: These coordinate deltas are (row, col) instead of (col, row), designed
# for interacting with AoC inputs read in line-by-line.
directions = namedtuple(
    'Directions',
    ('NORTH', 'EAST', 'SOUTH', 'WEST')
)(
    (-1, 0), (0, 1), (1, 0), (0, -1)
)
# This namedtuple is a mirror of above, with the tuple indexes being the
# opposite direction of their counterparts.
opposite_directions = namedtuple(
    'Directions',
    ('SOUTH', 'WEST', 'NORTH', 'EAST')
)(
    (1, 0), (0, -1), (-1, 0), (0, 1)
)

ordinal_directions = namedtuple(
    'OrdinalDirections',
    ('NORTH_EAST', 'SOUTH_EAST', 'SOUTH_WEST', 'NORTH_WEST'),
)(
    (-1, 1), (1, 1), (1, -1), (-1, -1)
)

# The below is a dictionary mapping operators to functions from the operator
# module, allowing for math (as well as comparisons, <, >, etc.) to be
# performed programatically without resorting to using eval(). For example,
# oper_map['+'](a, b) would be equivalent to running a + b. Note that this will
# not ensure you have int/float arguments, if a and b were '1' and '2',
# respectively, the result would be '12' (i.e. string concatenation).
#
# It should be noted that in-place operators do not update the first operand
# passed to them, so oper_map['+='](x, y) does not modify x in-place, but
# rather has the same result as oper_map['+'](x, y).
#
# See: https://docs.python.org/3/library/operator.html#in-place-operators
#
# All of these functions take two arguments, unliess otherwise indicated.
oper_map: dict[str, Callable[[Any, Any], Any]] = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    'is': operator.is_,
    'is not': operator.is_not,
    'abs': operator.abs,        # Takes single operand
    '+': operator.add,
    '+=': operator.iadd,
    '-': operator.sub,
    '-=': operator.isub,
    '*': operator.mul,
    '*=': operator.imul,
    '/': operator.truediv,      # Division (produces float result)
    '/=': operator.itruediv,
    '//': operator.floordiv,    # Floor division (produces int result)
    '//=': operator.ifloordiv,
    '&': operator.and_,
    '&=': operator.iand,
    '|': operator.or_,
    '|=': operator.ior,
    '^': operator.xor,
    '^=': operator.ixor,
}


@dataclass(frozen=True)
class Coordinate:
    '''
    Dataclass representing a single 2D coordinate
    '''
    x: float
    y: float

    @property
    def as_tuple(self) -> tuple[float, float]:
        '''
        Return the contents of this dataclass as tuple
        '''
        return self.x, self.y

    @property
    def neighbors(self) -> Iterator[Coordinate]:
        '''
        Return the neighboring Coordinates
        '''
        for direction in directions:
            yield Coordinate(self.x + direction[0], self.y + direction[1])


@dataclass(frozen=True)
class Coordinate3D:
    '''
    Dataclass representing a single 3D coordinate
    '''
    x: float
    y: float
    z: float

    @property
    def as_tuple(self) -> tuple[float, float, float]:
        '''
        Return the contents of this dataclass as tuple
        '''
        return self.x, self.y, self.z

    def distance_from(self, other: Coordinate3D) -> int:
        '''
        Return the Manhattan distance between this coordinate and another
        '''
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __add__(self, other: Coordinate3D) -> Coordinate3D:
        '''
        Add the X, Y, and Z params of both objects, returning a new object
        '''
        return Coordinate3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )


@dataclass(frozen=True)
class LineSegment:
    '''
    Represents a 2D line segment
    '''
    first: Coordinate
    second: Coordinate

    def __and__(self, other: LineSegment) -> Coordinate | None:
        '''
        Implements the & operator, returning the point at which the two lines
        intersect with one another, or None if there is no intersection.

        See https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line

        Imagining 2 line segments:

            (19, 13) -> (17, 14)    a.k.a. (x₁, y₁) -> (x₂, y₂)
            (18, 19) -> (17, 18)    a.k.a. (x₃, y₃) -> (x₄, y₄)

        '''
        x1, y1 = self.first.as_tuple
        x2, y2 = self.second.as_tuple
        x3, y3 = other.first.as_tuple
        x4, y4 = other.second.as_tuple

        divisor = ((x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4))
        if not divisor:
            # No intersection
            return None

        detx = (
            (((x1*y2 - y1*x2) * (x3-x4)) - ((x1-x2) * (x3*y4 - y3*x4))) /
            divisor
        )
        dety = (
            (((x1*y2 - y1*x2) * (y3-y4)) - ((y1-y2) * (x3*y4 - y3*x4))) /
            divisor
        )

        return Coordinate(detx, dety)

    def intersection(self, other: LineSegment) -> Coordinate3D | None:
        '''
        Same as the & operator
        '''
        return self & other




@dataclass(frozen=True)
class LineSegment3D:
    '''
    Represents a 3D line segment
    '''
    first: Coordinate3D
    second: Coordinate3D

    def __and__(self, other: LineSegment3D) -> Coordinate3D | None:
        '''
        Implements the & operator, returning the point at which the two lines
        intersect with one another, or None if there is no intersection.

        Thanks to this video for the formula: https://youtu.be/N-qUfr-rz_Y

        Imagining 2 line segments:

            (5, 2, -1) -> (1, -2, -3)
            (2, 0, 4)  -> (1, 2, -1)

        These form a system of 3 equations with 2 unknowns (α & β), one
        equation each for the x, y, and z values. Each equation takes the form
        of the first point's value as an integer, plus the product of an
        unknown and the second point's value. Using the above 2 line segments,
        these equations would be:

             5 + 1α = 2 + β
             2 - 2α = 0 + 2β
            -1 - 3α = 4 - 1β

        The first step to solving this system of equations is to move the
        integer values to the right side of the equations, and the unknowns to
        the left. Along with removing values that cancel out (the zero and any
        1 multipliers), This gives us:

              α - β = -3
           -2α - 2β = -2
            -3α + β = 5

        To solve for α and β, we'll pick two equations and ignore the third
        (for now). The next thing to do is to pick one of the unknowns and
        remove the multiplier (using division). Picking α, the first equation
        already has a single multiplier, so we can divide the entire second
        equation by 2, giving us the below two equations:

              α - β = -3
             -α - β = -1

        At this point, we want to make sure that the α in the second equation
        is the opposite sign as the first. It already is here, but if it were
        not then we could make it negative by multiplying everything in the
        equation by -1.

        We can now add the two equations together, which will cancel out α and
        leave us with:

                -2β = -4
                 2β = 4
                  β = 2

        With our β, calculated, we can plug it into any of our simplified
        equations from the previous step:

              α - 2 = -3
                  α = -1

        Finally, with both α and β known, go back to the third equation (the
        one that we were ignoring). If this equation works with our α and β,
        then the two lines intersect.

            -3α + β = 5
         -3(-1) + 2 = 5
              3 + 2 = 5
                  5 = 5

        These lines intersect, because the 3rd equation works with our α or β.
        To calculate the point of intersection, pick either of the two line
        segments and use either α or β (α if the first line segment, β if the
        second line segment). Let's choose the first line segment. The
        intersection can be calculated as (x₁ + α*x₂, y₁ + α*y₂, z₁ + α*z₂),
        where the subscript 1 is from the first point in the line segment, and
        the subscript 2 is from the second point in the line segment. This
        would be:

            (5 + -1(1), 2 + -1(-2), -1 + -1(-3))

            or (4, 4, 2)

        '''
        # Gather the integer constants from the first and second equations on
        # the "right" side.
        const0 = other.first.x - self.first.x
        const1 = other.first.y - self.first.y
        const2 = other.first.z - self.first.z
        # Gather the multipliers for alpha and beta on the "left" side.
        alpha_multiplier0 = self.second.x
        beta_multiplier0 = -other.second.x
        alpha_multiplier1 = self.second.y
        beta_multiplier1 = -other.second.y
        alpha_multiplier2 = self.second.z
        beta_multiplier2 = -other.second.z
        # Divide all multipliers and constants by the alpha-multiplier for the
        # first equation.
        alpha_multiplier0, beta_multiplier0, const0 = map(
            lambda a: a / alpha_multiplier0,
            (alpha_multiplier0, beta_multiplier0, const0)
        )
        # Repeat for the second equation, but then reverse the sign. This will
        # produce a first equation that is alpha + something, and a second
        # equation that is -alpha - something.
        alpha_multiplier1, beta_multiplier1, const1 = map(
            lambda a: -(a / alpha_multiplier1),
            (alpha_multiplier1, beta_multiplier1, const1)
        )
        # Now that we have performed the above, we can add the two equations
        # together and divide by the sum of the beta multipliers. The alpha
        # multipliers will cancel out.
        beta = (const0 + const1) / (beta_multiplier0 + beta_multiplier1)
        # Alpha can now be calculated by substituting beta in either of the
        # first two equations and then dividing by its alpha mulitplier.
        alpha = (const0 - (beta_multiplier0 * beta)) / alpha_multiplier0

        if (alpha_multiplier2 * alpha) + (beta_multiplier2 * beta) != const2:
            # No intersection
            return None

        return Coordinate3D(
            self.first.x + (alpha * self.second.x),
            self.first.y + (alpha * self.second.y),
            self.first.z + (alpha * self.second.z),
        )

    def intersection(self, other: LineSegment3D) -> Coordinate3D | None:
        '''
        Same as the & operator
        '''
        return self & other


class TupleMixin:
    '''
    Adds functions to do things to tuples. Because I don't like writing a bunch
    of map statements.
    '''
    @staticmethod
    def tuple_add(t1: tuple[int, ...], t2: tuple[int, ...]) -> tuple[int, ...]:
        '''
        Add each element of both tuples, returning a new tuple
        '''
        return tuple(map(lambda a, b: a + b, t1, t2))

    @staticmethod
    def tuple_subtract(t1: tuple[int, ...], t2: tuple[int, ...]) -> tuple[int, ...]:
        '''
        Add each element of both tuples, returning a new tuple
        '''
        return tuple(map(lambda a, b: a - b, t1, t2))

    @staticmethod
    def tuple_multiply_all(data: tuple[int, ...], factor: int) -> tuple[int, ...]:
        '''
        Multiply all items in the tuple by the given factor
        '''
        return tuple(map(lambda i: i * factor, data))


class XYMixin:
    '''
    Functions to do calculations on XY coordinates
    '''
    @staticmethod
    def distance(p1: XY, p2: XY) -> int:
        '''
        Calculate the number of steps between two coordinates (i.e. the
        Manhattan Distance)
        '''
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def perimeter(self, bounds: list[XY]) -> int:
        '''
        Calculate the lenth of the perimeter of a polygon, given a list of
        coordinates in either clockwise or counter-clockwise order.
        '''
        return sum(
            self.distance(bounds[n], bounds[n + 1])
            for n in range(len(bounds) - 1)
        ) + self.distance(bounds[-1], bounds[0])

    @staticmethod
    def shoelace(bounds: list[XY]) -> float:
        '''
        NOTE: bounds must be a list of coordinates in either clockwise or
        counter-clockwise order.

        The area A would be calculated as follows:

            2A = Σ|row(x)*col(x+1) - row(x+1)*col(x)|

        or:

            A = 1/2 * Σ|row(x)*col(x+1) - row(x+1)*col(x)|

        This sum includes the final vertex being compared to the first one.
        To accomplish this in a pretty generator expression, this function
        instead starts by comparing list index -1 with 0, and finishes
        comparing the 2nd-to-last index with the first one. By doing so, it
        manages to compare all vertexes.
        '''
        return abs(
            sum(
                (bounds[n][0] * bounds[n - 1][1]) - (bounds[n - 1][0] * bounds[n][1])
                for n in range(len(bounds))
            ) / 2
        )

class MathMixin:
    '''
    Helpful general-purpose math functions
    '''
    @staticmethod
    def factors(number: int, limit: int = 0) -> Iterator[int]:
        '''
        Generator function to return the factors of a number

        If limit is nonzero, then the generator will only return factors which
        are less than the specified value.
        '''
        for candidate in range(
            1,
            limit + 1 if limit else int(math.sqrt(number)),
        ):
            if number % candidate == 0:
                yield candidate
                complement = number // candidate
                if not limit or complement <= limit:
                    yield complement

    @staticmethod
    def prime(number: int) -> bool:
        '''
        Check if a number is prime by attempting to calculate its integetr
        factors. If any factors are found, the number is non prime.
        '''
        for candidate in range(2, int(math.sqrt(number))):
            if number % candidate == 0:
                return False
        return True

    @staticmethod
    def cramer_2x2(  # pylint: disable=too-many-positional-arguments
        a1: int,
        b1: int,
        c1: int,
        a2: int,
        b2: int,
        c2: int,
    ) -> tuple[float, float]:
        '''
        https://www.chilimath.com/lessons/advanced-algebra/cramers-rule-with-two-variables

        This method can solve a system of equations in the following form:

            a₁x + b₁y = c₁
            a₂x + b₂y = c₂

        The values above slot into 3 matrices:

                ┌       ┐         ┌       ┐         ┌       ┐
            D = | a₁ b₁ |    Dx = | c₁ b₁ |    Dy = | a₁ c₁ |
                | a₂ b₂ |         | c₂ b₂ |         | a₂ c₂ |
                └       ┘         └       ┘         └       ┘

        To solve for x, divide the determinant of Dx by the determinant of D.
        To solve for y, divide the determinant of Dy by the determinant of D.

        For a matrix in the following format:

            ┌     ┐
            | a b |
            | c d |
            └     ┘

        The determinant is equal to:

            ad - bc

        Thus, we can represent the determinants using the following:

            D  = (a₁b₂ - b₁a₂)
            Dx = (c₁b₂ - b₁c₂)
            Dy = (a₁c₂ - c₁a₂)

        Solving for x can be done by dividing Dx by D, and solving for y can be
        done by dividing Dy by D.

        Here is an example from https://adventofcode.com/2024/day/13

        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400

        This can be written as the following two equations:

            94a + 22b = 8400
            34a + 67b = 5400

        Which form the following matrices

                ┌       ┐         ┌         ┐         ┌         ┐
            D = | 94 22 |    Dx = | 8400 22 |    Dy = | 94 8400 |
                | 34 67 |         | 5400 67 |         | 34 5400 |
                └       ┘         └         ┘         └         ┘

        Calculating the determinants yields:

            D  = (94*67) - (22*34) = 5550
            Dx = (8400 * 67) - (22*5400) = 444000
            Dy = (94 * 5400) - (8400*34) = 222000

        Solving for x and y:

            x = Dx / D = 444000 / 5550 = 80
            y = Dy / D = 222000 / 5550 = 40
        '''
        D: int = (a1 * b2) - (b1 * a2)
        Dx: int = (c1 * b2) - (b1 * c2)
        Dy: int = (a1 * c2) - (c1 * a2)

        return (Dx / D), (Dy / D)


class Grid(TupleMixin, XYMixin):
    '''
    Manage a grid as a list of list of strings. Can be indexed like a 2D array.

    Optonally, a callback can be passed when initializing. This callback will
    be run on each column of each line. This can be used to, for example, turn
    each column into an int. For example:

        grid = Grid(path, lambda col: int(col))
    '''
    def __init__(
        self,
        data: Path | str | Sequence[str],
        row_cb: Callable[[str], Any] = lambda col: col,
        neighbor_order: Directions = directions,
    ) -> None:
        '''
        Load the file from the Path object
        '''
        self.data = []
        try:
            fh = data.open()
        except AttributeError:
            if isinstance(data, str):
                # If input was a string, split it into a list of strings
                self.data = [
                    [row_cb(col) for col in line.rstrip()]
                    for line in data.splitlines()
                ]
            else:
                # Assume grid data is a pre-assembled list of lists
                self.data = data
        else:
            self.data = [
                [row_cb(col) for col in line.rstrip()]
                for line in fh
            ]
            fh.close()
        self.rows = len(self.data)
        self.cols = max(len(row) for row in self.data)
        self.max_row = self.rows - 1
        self.max_col = self.cols - 1

        self.directions: Directions = neighbor_order
        self.opposite_directions: Directions = tuple(
            tuple(-1 * x for x in nesw)
            for nesw in self.directions
        )
        self.initial_state = copy.deepcopy(self.data)

    def __contains__(self, coord: XY) -> bool:
        '''
        Return True if the coordinate is within the bounds of the grid
        '''
        return 0 <= coord[0] <= self.max_row and 0 <= coord[1] <= self.max_col

    def __getitem__(self, index: int | XY) -> list[Any]:
        '''
        If index is an integer, return that index's row.

        If index is a tuple, return the value at that row/column.
        '''
        if isinstance(index, int):
            return self.data[index]

        if index not in self:
            raise IndexError(f'Coordinate {index!r} is outside of grid')

        try:
            return self.data[index[0]][index[1]]
        except IndexError:
            # My vim configuration deletes trailing whitespace on buffer write.
            # So, it is possible to have a valid coordinate that is within the
            # bounds of the grid, but the column position is past the end of
            # the row, because that line of the puzzle input ended in
            # whitespace. Return a space to simulate an empty space at this
            # position.
            return ' '

    def __setitem__(self, coord: XY, val: str) -> None:
        '''
        Set a tile by coordinate
        '''
        if not isinstance(coord, tuple):
            raise ValueError(f"Expected coordinate pair, not {coord!r}")

        self.data[coord[0]][coord[1]] = val

    def reset(self) -> None:
        '''
        Reset to the initial state
        '''
        self.data = copy.deepcopy(self.initial_state)

    def row(self, index: int) -> Any:
        '''
        Return the specified row
        '''
        return self.data[index]

    def neighbors(self, coord: XY) -> Iterator[tuple[XY, Any]]:
        '''
        Generator which yields a tuple of each neigbboring coordinate and the
        value stored at that coordinate.
        '''
        delta: XY
        for delta in self.directions:
            neighbor: XY = self.tuple_add(coord, delta)
            if neighbor in self:
                yield neighbor, self[neighbor]

    def tile_iter(self) -> Iterator[tuple[XY, str]]:
        '''
        Similar to enumerate(), but instead of yielding a sequence of ints
        paired with contents, the first element of each yielded tuple is the
        coordinate.
        '''
        for row in range(self.rows):
            for col in range(self.cols):
                yield (row, col), self.data[row][col]

    def column_iter(self) -> Iterator[str]:
        '''
        Generator which yields the contents of the grid one column at a time
        '''
        for col in range(self.cols):
            yield ''.join(
                str(self.data[row][col])
                for row in range(self.rows)
            )

    def find(self, value: Any) -> XY | None:
        '''
        Return the first row/column pair that matches the specified value, or
        None if there is no match.
        '''
        for row_index, row in enumerate(self.data):
            for col_index, col in enumerate(row):
                if col == value:
                    return row_index, col_index

    def print(self) -> None:
        '''
        Print the grid to stdout
        '''
        for row in self.data:
            sys.stdout.write(f'{"".join(str(x) for x in row)}\n')
        sys.stdout.write('\n')
        sys.stdout.flush()

    def counter(self, row_start: int = 0) -> Counter:
        """
        Returns a Counter object that summarizes the contents of the Grid
        """
        return Counter(
            tile for (row, _), tile in self.tile_iter()
            if row >= row_start
        )

    def sha256(self) -> str:
        """
        Produces a sha256 hash of the contents of the grid
        """
        return hashlib.sha256(
            ''.join(t[1] for t in self.tile_iter()).encode()
        ).hexdigest()


class InfiniteGrid(Grid):
    '''
    A modified Grid class which acts like a normal Grid in every way but in
    indexing and neighbor detection. For these, it is assumed that the grid
    content repeats infinitely in every direction.
    '''
    def __getitem__(self, index: XY) -> Any:
        '''
        Return the single item at that row/column coordinate's location.
        '''
        row, col = index
        return self.data[row % self.rows][col % self.cols]

    def neighbors(self, coord: XY) -> Iterator[tuple[XY, Any]]:
        '''
        Generator which yields a tuple of each neigbboring coordinate and the
        value stored at that coordinate.
        '''
        row, col = coord
        for (row_delta, col_delta) in self.directions:
            new_row, new_col = row + row_delta, col + col_delta
            yield (new_row, new_col), self[(new_row, new_col)]


class AOC:
    '''
    Base class for Advent of Code submissions
    '''
    # These all must be overridden in a subclass
    year: int = 0
    day: int = 0
    example_data: str = ''
    example_data_part1: str = ''
    example_data_part2: str = ''

    def __init__(self, example: bool = False) -> None:
        '''
        Create Path object for the input file
        '''
        self.example: bool = example
        try:
            self.year, self.day = (
                int(n) for n in re.match(
                    r'AOC(\d{4})Day(\d{1,2})',
                    self.__class__.__name__,
                ).groups()
            )
        except AttributeError:
            pass

        if hasattr(self, 'post_init'):
            self.post_init()

    @functools.cached_property
    def input(self) -> str:
        '''
        Load the puzzle input, removing trailing newline from file. For multi-line
        inputs, this has no impact on .splitlines(), but for single-line
        inputs, it prevents us from needing to rstrip() in the puzzle code.
        '''
        if not self.example:
            return Path(__file__).parent.parent.joinpath(
                'inputs',
                str(self.year),
                f'day{str(self.day).zfill(2)}.txt',
            ).read_text().rstrip('\n')

        return self.example_data.strip('\n')

    @property
    def input_part1(self) -> str:
        '''
        Disambiguation that accounts for cases where the example data for part
        two is different from part one.
        '''
        if not self.example:
            return self.input

        return self.example_data_part1.strip('\n')

    @property
    def input_part2(self) -> str:
        '''
        Disambiguation that accounts for cases where the example data for part
        two is different from part one.
        '''
        if not self.example:
            return self.input

        return self.example_data_part2.strip('\n')

    @staticmethod
    def timed_exec(
        label: str,
        func: Callable[[], Any],
    ) -> None:
        '''
        Time the function
        '''
        start: float = time.time()
        ret: Callable = func()
        total: float = time.time() - start
        print(f'{label}: {ret} ({total} seconds)')  # pylint: disable=no-member

    def run(self):
        '''
        Run both parts and print the results
        '''
        # Optionally validate input
        if '-v' in sys.argv:
            if any(hasattr(self, f'validate_part{n}') for n in (1, 2)):
                example: AOC = self.__class__(example=True)
                part: int
                for part in (1, 2):
                    try:
                        expected: Any = getattr(self, f'validate_part{part}')
                    except AttributeError:
                        continue

                    result: Any = getattr(example, f'part{part}')()
                    if result != expected:
                        sys.stderr.write(
                            f'Validation failed for Part {part}! '
                            f'Expected {expected}, got {result}\n'
                        )
                        sys.exit(1)

        header: str = f'Result for Day {self.day}'

        print(header)
        print('-' * len(header))
        for part in (1, 2):
            if hasattr(self, f'part{part}'):
                self.timed_exec(f'Answer {part}', getattr(self, f'part{part}'))
            if hasattr(self, f'part{part}_alt'):
                self.timed_exec(
                    f'Answer {part} (alternate solution)',
                    getattr(self, f'part{part}_alt'),
                )
