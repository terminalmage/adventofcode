#!/usr/bin/env python
'''
https://adventofcode.com/2022/day/22

--- Day 22: Monkey Map ---

The monkeys take you on a surprisingly easy trail through the jungle. They're
even going in roughly the right direction according to your handheld device's
Grove Positioning System.

As you walk, the monkeys explain that the grove is protected by a force field.
To pass through the force field, you have to enter a password; doing so
involves tracing a specific path on a strangely-shaped board.

At least, you're pretty sure that's what you have to do; the elephants aren't
exactly fluent in monkey.

The monkeys give you notes that they took when they last saw the password
entered (your puzzle input).

For example:

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

The first half of the monkeys' notes is a map of the board. It is comprised of
a set of open tiles (on which you can move, drawn .) and solid walls (tiles
which you cannot enter, drawn #).

The second half is a description of the path you must follow. It consists of
alternating numbers and letters:

- A number indicates the number of tiles to move in the direction you are
  facing. If you run into a wall, you stop moving forward and continue with the
  next instruction.

- A letter indicates whether to turn 90 degrees clockwise (R) or
  counterclockwise (L). Turning happens in-place; it does not change your
  current tile.

So, a path like 10R5 means "go forward 10 tiles, then turn clockwise 90
degrees, then go forward 5 tiles".

You begin the path in the leftmost open tile of the top row of tiles.
Initially, you are facing to the right (from the perspective of how the map is
drawn).

If a movement instruction would take you off of the map, you wrap around to the
other side of the board. In other words, if your next tile is off of the board,
you should instead look in the direction opposite of your current facing as far
as you can until you find the opposite edge of the board, then reappear there.

For example, if you are at A and facing to the right, the tile in front of you
is marked B; if you are at C and facing down, the tile in front of you is
marked D:

        ...#
        .#..
        #...
        ....
...#.D.....#
........#...
B.#....#...A
.....C....#.
        ...#....
        .....#..
        .#......
        ......#.

It is possible for the next tile (after wrapping around) to be a wall; this
still counts as there being a wall in front of you, and so movement stops
before you actually wrap to the other side of the board.

By drawing the last facing you had with an arrow on each tile you visit, the
full path taken by the above example looks like this:

        >>v#
        .#v.
        #.v.
        ..v.
...#...v..v#
>>>v...>#.>>
..#v...#....
...>>>>v..#.
        ...#....
        .....#..
        .#......
        ......#.

To finish providing the password to this strange input device, you need to
determine numbers for your final row, column, and facing as your final position
appears from the perspective of the original map. Rows start from 1 at the top
and count downward; columns start from 1 at the left and count rightward. (In
the above example, row 1, column 1 refers to the empty space with no tile on it
in the top-left corner.) Facing is 0 for right (>), 1 for down (v), 2 for left
(<), and 3 for up (^). The final password is the sum of 1000 times the row, 4
times the column, and the facing.

In the above example, the final row is 6, the final column is 8, and the final
facing is 0. So, the final password is 1000 * 6 + 4 * 8 + 0: 6032.

Follow the path given in the monkeys' notes. What is the final password?

--- Part Two ---

As you reach the force field, you think you hear some Elves in the distance.
Perhaps they've already arrived?

You approach the strange input device, but it isn't quite what the monkeys drew
in their notes. Instead, you are met with a large cube; each of its six faces
is a square of 50x50 tiles.

To be fair, the monkeys' map does have six 50x50 regions on it. If you were to
carefully fold the map, you should be able to shape it into a cube!

In the example above, the six (smaller, 4x4) faces of the cube are:

        1111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

You still start in the same position and with the same facing as before, but
the wrapping rules are different. Now, if you would walk off the board, you
instead proceed around the cube. From the perspective of the map, this can look
a little strange. In the above example, if you are at A and move to the right,
you would arrive at B facing down; if you are at C and move down, you would
arrive at D facing up:

        ...#
        .#..
        #...
        ....
...#.......#
........#..A
..#....#....
.D........#.
        ...#..B.
        .....#..
        .#......
        ..C...#.

Walls still block your path, even if they are on a different face of the cube.
If you are at E facing up, your movement is blocked by the wall marked by the
arrow:

        ...#
        .#..
     -->#...
        ....
...#..E....#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

Using the same method of drawing the last facing you had with an arrow on each
tile you visit, the full path taken by the above example now looks like this:

        >>v#
        .#v.
        #.v.
        ..v.
...#..^...v#
.>>>>>^.#.>>
.^#....#....
.^........#.
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#.

The final password is still calculated from your final position and facing from
the perspective of the map. In this example, the final row is 5, the final
column is 7, and the final facing is 3, so the final password is 1000 * 5 + 4 *
7 + 3 = 5031.
'''
import functools
import math
import re
from dataclasses import dataclass

# Local imports
from aoc import AOC

# Typing shortcuts
Coordinate = tuple[int, int]

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
    day = 22
    width = 7

    def __init__(self, example: bool = False) -> None:
        '''
        Load the jet pattern and define the rock sequence. The reset_chamber()
        function will create new itertools.cycle instances for both, which
        allow them to be repeated in a loop for as long as we need.
        '''
        super().__init__(example=example)

        lines = self.input.read_text().splitlines()
        path_lines = lines[:-2]
        moves = lines[-1]

        lengths = [len(line) for line in path_lines]
        self.width = max(*lengths)
        self.height = len(lengths)
        # The length of each side of each face
        self.face_size = math.gcd(*lengths)

        # Assign the input to the grid
        self.grid = {}
        for row, line in enumerate(path_lines):
            for col, char in enumerate(line.rstrip()):
                if char in (PATH, WALL):
                    self.grid[(col, row)] = char

        # Mapping of directions to the x/y delta used to move in that direction
        self.move_deltas = {
            0: (1, 0),   # right
            1: (0, 1),   # down
            2: (-1, 0),  # left
            3: (0, -1),  # up
        }

        # Reduce coordinate into a "face" coordinate
        # e.g. (50, 100) becomes (1, 2) for a face_size of 50
        _coord_to_face = lambda coord: tuple(x // self.face_size for x in coord)

        # Assign adjacent faces that we can derive simply from analyzing where
        # path/wall characters exist in the grid. The "faces" attribute here
        # is a dictionary mapping faces to their neighbors in each direction. A
        # face is identified by its (x, y) positions, where x, y are the
        # coordinate positions divided by the face size. For example, given a
        # face size of 50, face (1, 2) would have a top-left corner located at
        # (50, 100), and a bottom-right corner located at (99, 149).
        self.faces = {}
        for row in range(0, self.height, self.face_size):
            for col in range(0, self.width, self.face_size):
                # This coordinate is the top-left of a given face
                coord = (col, row)
                if coord in self.grid:
                    face_coord = _coord_to_face(coord)
                    # There is a face at this location. Check for
                    # directly-adjacent faces using the offsets defined above
                    for direction, move_delta in self.move_deltas.items():
                        # Add the offsets to the current coordinate. This will
                        # result in "neighbor" containing the top-left
                        # coordinate of the face in that direction.
                        offset = tuple(map(lambda x: self.face_size * x, move_delta))
                        neighbor = tuple(sum(x) for x in zip(coord, offset))
                        # If the face exists, assign it to the coordinate
                        if neighbor in self.grid:
                            self.faces.setdefault(
                                face_coord, [None, None, None, None]
                            )[direction] = _coord_to_face(neighbor)

        def _get_relative(
            face: Coordinate,
            relative_to: int | Coordinate,
            delta: int = 0,
        ) -> Coordinate | None:
            '''
            Get the face, if known, that is the specified directional delta
            relative to the specified direction (or other coordinate)
            '''
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
                        # right of C. if the position of the shared face is not
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
        self.path = tuple(re.findall(r'(?:\d+|[RL])', moves))

        # The leftmost column of the first row
        self.start = (self.col_bounds(0).min, 0)

        # Initialize position and direction
        self.reset()

    def reset(self) -> None:
        '''
        Reset position and direction
        '''
        # pylint: disable=attribute-defined-outside-init
        self.position = self.start
        # Face to the right
        self.direction = 0
        # pylint: enable=attribute-defined-outside-init

    @property
    def password(self) -> int:
        '''
        Return the current password, calculated as a combination of position
        and direction. The formula is:

            (1000 * row) + (4 * column) + direction

        NOTE: In self.grid, rows and columns are zero-indexed, but for the
        purpose of password calculation they need to be one-indexed.
        '''
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
    def move_delta(self) -> Coordinate:
        '''
        Return the x, y delta to move in the current direction
        '''
        return self.move_deltas[self.direction]

    def get_face(self, position: Coordinate):
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
        edge_offsets = (
            (0,0),
            (self.face_size-1, 0),
            (self.face_size-1,self.face_size-1),
            (0, self.face_size-1),
        )
        self.reset()

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
                        if new_pos in self.grid:
                            # Direction is not changing because we are not
                            # wrapping around the cube
                            new_dir = self.direction
                        else:
                            # Discover the correct offset to apply in the
                            # translation
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

                            #import pudb; pu.db
                            new_face = self.faces[self.current_face][self.direction]
                            new_dir = (self.faces[new_face].index(self.current_face) + 2) % 4
                            new_pos = tuple(
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
                        self.position = new_pos
                        self.direction = new_dir

        return self.password


if __name__ == '__main__':
    # Run against test data
    aoc = AOC2022Day22(example=True)
    aoc.validate(aoc.part1(), 6032)
    aoc.validate(aoc.part2(), 5031)
    # Run against actual data
    aoc = AOC2022Day22(example=False)
    aoc.run()
