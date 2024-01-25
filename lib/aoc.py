'''
Base class for Advent of Code submissions
'''
import functools
import operator
import re
import sys
import time
from collections import namedtuple
from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

# Type hints
XY = tuple[float, float]
XYZ = tuple[float, float, float]

# NOTE: These coordinate deltas are (row, col) instead of (col, row), designed
# for interacting with AoC inputs read in line-by-line.
directions = namedtuple(
    'Directions',
    ('NORTH', 'SOUTH', 'WEST', 'EAST')
)(
    (-1, 0), (1, 0), (0, -1), (0, 1)
)
# This namedtuple is a mirror of above, with the tuple indexes being the
# opposite direction of their counterparts.
opposite_directions = namedtuple(
    'Directions',
    ('SOUTH', 'NORTH', 'EAST', 'WEST')
)(
    (1, 0), (-1, 0), (0, 1), (0, -1)
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
    def neighbors(self) -> Generator[Self, None, None]:
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


@dataclass(frozen=True)
class LineSegment:
    '''
    Represents a 2D line segment
    '''
    first: Coordinate
    second: Coordinate

    def __and__(self, other: Self) -> Coordinate | None:
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

    def intersection(self, other: Self) -> Coordinate3D | None:
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

    def __and__(self, other: Self) -> Coordinate3D | None:
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

    def intersection(self, other: Self) -> Coordinate3D | None:
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


class Grid:
    '''
    Manage a grid as a list of list of strings. Can be indexed like a 2D array.

    Optonally, a callback can be passed when initializing. This callback will
    be run on each column of each line. This can be used to, for example, turn
    each column into an int. For example:

        grid = Grid(path, lambda col: int(col))
    '''
    directions: namedtuple = directions
    opposite_directions: namedtuple = opposite_directions

    def __init__(
        self,
        data: Path | str | Sequence[str],
        row_cb: Callable[[str], Any] = lambda col: col,
    ) -> None:
        '''
        Load the file from the Path object
        '''
        self.data = []
        try:
            fh = data.open()
        except AttributeError:
            if isinstance(data, str):
                # If input was a string, split it into a list of strings.
                # Otherwise, we will assume that data is an iterable sequence
                # of strings.
                data = data.splitlines()

            self.data = [
                [row_cb(col) for col in line.rstrip()]
                for line in data
            ]
        else:
            self.data = [
                [row_cb(col) for col in line.rstrip()]
                for line in fh
            ]
            fh.close()
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.max_row = self.rows - 1
        self.max_col = self.cols - 1

    def __contains__(self, coord: XY) -> bool:
        '''
        Return True if the coordinate is within the bounds of the grid
        '''
        return 0 <= coord[0] <= self.max_row and 0 <= coord[1] <= self.max_col

    def __getitem__(self, index: int | XY) -> list[Any]:
        '''
        If index is an integer, return that index's row.

        If index is a Coordinate, return the single item at that row/column
        coordinate's location.
        '''
        try:
            row, col = index
            return self.data[row][col]
        except (TypeError, ValueError):
            return self.data[index]

    def neighbors(
        self,
        coord: XY,
    ) -> Generator[tuple[XY, Any], None, None]:
        '''
        Generator which yields a tuple of each neigbboring coordinate and the
        value stored at that coordinate.
        '''
        row, col = coord
        for (row_delta, col_delta) in self.directions:
            neighbor: XY = row + row_delta, col + col_delta
            if neighbor in self:
                yield neighbor, self[neighbor]

    def column_iter(self) -> Generator[str, None, None]:
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
            for col_index in range(self.cols):
                if row[col_index] == value:
                    return row_index, col_index

    def print(self) -> None:
        '''
        Print the grid to stdout
        '''
        for row in self.data:
            sys.stdout.write(f'{"".join(str(x) for x in row)}\n')
        sys.stdout.write('\n')
        sys.stdout.flush()


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

    def neighbors(
        self,
        coord: XY,
    ) -> Generator[tuple[XY, Any], None, None]:
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
