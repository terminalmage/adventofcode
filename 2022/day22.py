#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/22
'''
import functools
import math
import re
import textwrap
from dataclasses import dataclass
from collections.abc import Callable

# Local imports
from aoc import AOC, XY

PATH = '.'
WALL = '#'


@dataclass
class Bounds:
    '''
    Stores min/max values
    '''
    min: int
    max: int


class AOC2022Day22(AOC):
    '''
    Day 22 of Advent of Code 2022
    '''
    example_data: str = textwrap.dedent(
        '''
                ...#
                .#..
                #...
                ....
        ...#.......#
        ........#...
        ..#....#....
        ..........#.
                ...#....
                .....#..
                .#......
                ......#.

        10R5L5R10L4R5L5
        '''
    )

    validate_part1: int = 6032
    validate_part2: int = 5031

    # Set by post_init
    width = None
    height = None
    face_size = None
    grid = None
    move_deltas = None
    faces = None
    path = None
    start = None
    position = None
    direction = None

    def post_init(self) -> None:
        '''
        Load the input and set everything up for the path traversal
        '''
        lines: list[str] = self.input.splitlines()
        path_lines: list[str] = lines[:-2]
        moves: str = lines[-1]

        lengths: list[int] = [len(line) for line in path_lines]
        self.width: int = max(*lengths)
        self.height: int = len(lengths)
        # The length of each side of each face
        self.face_size: int = math.gcd(*lengths)

        # Assign the input to the grid
        self.grid: dict[XY, str] = {}
        row: int
        col: int
        line: str
        char: str
        for row, line in enumerate(path_lines):
            for col, char in enumerate(line.rstrip()):
                if char in (PATH, WALL):
                    self.grid[(col, row)] = char

        # Mapping of directions to the x/y delta used to move in that direction
        self.move_deltas: dict[int, XY] = {
            0: (1, 0),   # right
            1: (0, 1),   # down
            2: (-1, 0),  # left
            3: (0, -1),  # up
        }

        # Reduce coordinate into a "face" coordinate
        # e.g. (50, 100) becomes (1, 2) for a face_size of 50
        _coord_to_face: Callable[[XY], XY] = lambda coord: tuple(
            x // self.face_size for x in coord
        )

        # Assign adjacent faces that we can derive simply from analyzing where
        # path/wall characters exist in the grid. The "faces" attribute here
        # is a dictionary mapping faces to their neighbors in each direction. A
        # face is identified by its (x, y) positions, where x, y are the
        # coordinate positions divided by the face size. For example, given a
        # face size of 50, face (1, 2) would have a top-left corner located at
        # (50, 100), and a bottom-right corner located at (99, 149).
        self.faces: dict[int, list[int]] = {}
        row: int
        col: int
        for row in range(0, self.height, self.face_size):
            for col in range(0, self.width, self.face_size):
                # This coordinate is the top-left of a given face
                coord: XY = (col, row)
                if coord in self.grid:
                    face_coord: XY = _coord_to_face(coord)
                    # There is a face at this location. Check for
                    # directly-adjacent faces using the offsets defined above
                    direction: int
                    move_delta: XY
                    for direction, move_delta in self.move_deltas.items():
                        # Add the offsets to the current coordinate. This will
                        # result in "neighbor" containing the top-left
                        # coordinate of the face in that direction.
                        offset: XY = tuple(map(lambda x: self.face_size * x, move_delta))
                        neighbor: XY = tuple(sum(x) for x in zip(coord, offset))
                        # If the face exists, assign it to the coordinate. Once
                        # each direction has been computed, self.faces will
                        # contain the face number corresponding the four
                        # directions from a given coordinate. The directions
                        # for each face number correspond to the directions
                        # defined above in self.move_deltas. So, for example,
                        # self.faces[(15, 12)][1] would contain the face number
                        # "down" from that coordinate.
                        if neighbor in self.grid:
                            self.faces.setdefault(
                                face_coord, [None, None, None, None]
                            )[direction] = _coord_to_face(neighbor)

        def _get_relative(
            face: XY,
            relative_to: int | XY,
            delta: int = 0,
        ) -> XY | None:
            '''
            Get the face, if known, that is the specified directional delta
            relative to the specified direction (or other coordinate)
            '''
            index: int
            if isinstance(relative_to, int):
                index = relative_to
            else:
                index = self.faces[face].index(relative_to)
            return self.faces[face][(index + delta) % 4]

        # Now that we know which faces are adjacent to each other, use that
        # information to map the rest of the directions for each face. Cycle
        # through each of the faces until everything is filled in.
        while any(None in face for face in self.faces.values()):
            for face in self.faces:  # pylint: disable=consider-using-dict-items
                for direction in self.move_deltas:
                    if self.faces[face][direction] is None:
                        # We don't know yet which face borders this face in
                        # this direction. To find out, we need to discover a
                        # known face which borders both this face and one of
                        # the face's adjacent (i.e. neighbor) faces.
                        #
                        # First, Look at the face in either direction of the
                        # current direction. This is the "neighbor_face". For
                        # example, if direction is "right", the neighbor faces
                        # are "up" and "down". If we don't know the neighbors
                        # yet, skip them (they will be discovered in a future
                        # loop iteration).
                        #
                        # Assuming we found the neighbor, we then get the
                        # original face's position relative to the neighbor,
                        # and apply the same rotational delta. The face to that
                        # direction from the neighbor is the shared face that
                        # is to the right of the original face.
                        #
                        # Take the following arrangement as an example:
                        #
                        #        AB
                        #        C
                        #       DE
                        #       F
                        #
                        # We don't know the face to the right of C yet, but we
                        # do know the face that is one position
                        # counter-clockwise (i.e. a rotational delta of -1).
                        # That face is face A. To find the face with which they
                        # both share an edge we first get C's relative position
                        # from A (i.e. "down"), and then apply the same
                        # counter-clockwise delta (giving us a direction of
                        # "right"). This means that the face to the right of C
                        # is the face which is also to the right of A. With
                        # this knowledge, we can determine that B is to the
                        # right of C. If the position of the shared face is not
                        # yet known, again skip it, as it will be discovered in
                        # a future loop iteration.
                        #
                        # Using the same principle we can also find
                        # the direction of C relative to B. Take the direction
                        # of the other side B has in common (A, which is to the
                        # left of B), and apply the counter-clockwise
                        # rotational delta, with a result of "down". So, when
                        # folded, C is below B.
                        #
                        # This can be repeated in both directions, for each
                        # face, until all neighbors of all faces are known.
                        for delta in (-1, 1):
                            neighbor = _get_relative(face, direction, delta)
                            if neighbor is None:
                                # We don't know this face (yet), skip for now
                                continue
                            shared_face = _get_relative(neighbor, face, delta)
                            if shared_face is None:
                                # We don't know this face (yet), skip for now
                                continue
                            # If we've gotten here, shared_face is adjacent to
                            # the current face (at direction "direction").
                            # Update self.faces accordingly.
                            shared_index = self.faces[shared_face].index(neighbor)
                            self.faces[shared_face][(shared_index + delta) % 4] = face
                            self.faces[face][direction] = shared_face

        # Load the path
        self.path: tuple[str, ...] = tuple(re.findall(r'(?:\d+|[RL])', moves))

        # The leftmost column of the first row
        self.start: XY = (self.col_bounds(0).min, 0)

        # Initialize position and direction
        self.reset()

    def reset(self) -> None:
        '''
        Reset position and direction
        '''
        self.position: XY = self.start
        # Face to the right (see self.move_deltas)
        self.direction: int = 0

    @property
    def password(self) -> int:
        '''
        Return the current password, calculated as a combination of position
        and direction. The formula is:

            (1000 * row) + (4 * column) + direction

        NOTE: In self.grid, rows and columns are zero-indexed, but for the
        purpose of password calculation they need to be one-indexed.
        '''
        col: int
        row: int
        col, row = [value + 1 for value in self.position]
        return (1000 * row) + (4 * col) + self.direction

    @functools.lru_cache
    def row_bounds(self, col: int) -> Bounds:
        '''
        Return a tuple of the minimum and maximum row for the specified column
        '''
        return Bounds(
            min(y for x, y in self.grid if x == col),
            max(y for x, y in self.grid if x == col),
        )

    @functools.lru_cache
    def col_bounds(self, row: int) -> Bounds:
        '''
        Return a tuple of the minimum and maximum row for the specified column
        '''
        return Bounds(
            min(x for x, y in self.grid if y == row),
            max(x for x, y in self.grid if y == row),
        )

    @property
    def move_delta(self) -> XY:
        '''
        Return the x, y delta to move in the current direction
        '''
        return self.move_deltas[self.direction]

    def get_face(self, position: XY):
        '''
        Get the face corresponding to the coordinates passed in

        Reduces coordinate into a "face" coordinate

        e.g. (50, 100) becomes (1, 2) for a face_size of 50
        '''
        return tuple(x // self.face_size for x in position)

    @property
    def current_face(self):
        '''
        Returns the current face
        '''
        return self.get_face(self.position)

    def part1(self) -> int:
        '''
        Return the password corresponding to the final coordinates
        '''
        # pylint: disable=attribute-defined-outside-init
        self.reset()
        move: str
        for move in self.path:
            match move:
                case 'L':
                    self.direction = (self.direction - 1) % 4
                case 'R':
                    self.direction = (self.direction + 1) % 4
                case _:
                    for _ in range(int(move)):
                        new_pos = tuple(
                            sum(x) for x in zip(self.position, self.move_delta)
                        )
                        if new_pos not in self.grid:
                            col_bounds = self.col_bounds(self.position[1])
                            row_bounds = self.row_bounds(self.position[0])
                            # Handle wrapping around grid
                            if new_pos[0] < col_bounds.min:
                                new_pos = (col_bounds.max, new_pos[1])
                            elif new_pos[0] > col_bounds.max:
                                new_pos = (col_bounds.min, new_pos[1])
                            elif new_pos[1] < row_bounds.min:
                                new_pos = (new_pos[0], row_bounds.max)
                            elif new_pos[1] > row_bounds.max:
                                new_pos = (new_pos[0], row_bounds.min)
                            else:
                                # Shouldn't get here but just in case
                                raise RuntimeError(
                                    f'Failed to wrap around from '
                                    f'{self.position!r}'
                                )

                        if self.grid[new_pos] == WALL:
                            # Wall is blocking further movement, stop moving
                            break

                        # Update the current position to the new one and jump
                        # back to the beginning of the loop to continue moving
                        # (or make a left/right turn)
                        self.position = new_pos

        return self.password

    def part2(self) -> int:
        '''
        Return the password corresponding to the final coordinates

        NOTE: The cube wrapping code was adapted from /u/RedTwinkleToes
              (https://old.reddit.com/r/adventofcode/comments/zsct8w/2022_day_22_solutions/j17yjcz/)
        '''
        # pylint: disable=attribute-defined-outside-init
        edge_offsets: XY = (
            (0,0),
            (self.face_size-1, 0),
            (self.face_size-1,self.face_size-1),
            (0, self.face_size-1),
        )
        self.reset()

        move: str
        for move in self.path:
            match move:
                case 'L':
                    self.direction = (self.direction - 1) % 4
                case 'R':
                    self.direction = (self.direction + 1) % 4
                case _:
                    for _ in range(int(move)):
                        new_pos: XY = tuple(
                            sum(x) for x in zip(self.position, self.move_delta)
                        )
                        if new_pos in self.grid:
                            # Direction is not changing because we are not
                            # wrapping around the cube
                            new_dir: int = self.direction
                        else:
                            # Discover the correct offset to apply in the
                            # translation
                            corner_offset: int
                            for corner_offset in range(self.face_size):
                                if tuple(
                                    (face_offset * self.face_size) + edge_offset
                                    + (move_delta * corner_offset)
                                    for face_offset, edge_offset, move_delta in
                                    zip(
                                        self.current_face,
                                        edge_offsets[(self.direction + 1) % 4],
                                        self.move_deltas[(self.direction + 1) % 4],
                                    )
                                ) == self.position:
                                    break
                            else:
                                raise RuntimeError(
                                    f'Failed to find the proper corner offset '
                                    f'when wrapping from {self.position}'
                                )

                            new_face: int = self.faces[self.current_face][self.direction]
                            new_dir: int = \
                                (self.faces[new_face].index(self.current_face) + 2) % 4
                            new_pos: XY = tuple(
                                (face_offset * self.face_size) + edge_offset
                                + (move_delta * corner_offset)
                                for face_offset, edge_offset, move_delta in
                                zip(
                                    new_face,
                                    edge_offsets[new_dir],
                                    self.move_deltas[(new_dir + 1) % 4],
                                )
                            )

                        if self.grid[new_pos] == WALL:
                            # Wall is blocking further movement, stop moving
                            break

                        # Update the current position to the new one and jump
                        # back to the beginning of the loop to continue moving
                        # (or make a left/right turn)
                        self.position: XY = new_pos
                        self.direction: int = new_dir

        return self.password


if __name__ == '__main__':
    aoc = AOC2022Day22()
    aoc.run()
