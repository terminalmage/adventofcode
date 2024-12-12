#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/12
'''
import textwrap
from collections.abc import Iterator

# Local imports
from aoc import AOC, Grid, XY


class Region:
    '''
    Gathers a set of plots of the same crop that are contiguous
    '''
    def __init__(self, plots: frozenset[XY], parent: 'Farm') -> None:
        '''
        Initialize the object
        '''
        self.plots = plots
        self.parent = parent
        self.crop = parent[next(iter(plots))]

    def __repr__(self) -> str:
        '''
        Define repr() output
        '''
        return f'Region(crop={self.crop!r}, plots={self.plots!r})'

    @property
    def area(self) -> int:
        '''
        The area of the Region (i.e. the number of plots)
        '''
        return len(self.plots)

    @property
    def perimeter(self) -> int:
        '''
        Calculate the perimeter of this Region
        '''
        ret: int = 0

        coord: XY
        for coord in self.plots:
            neighbors: list[tuple[XY, str]] = list(self.parent.neighbors(coord))
            ret += sum(
                1 for xy, crop in neighbors
                if crop != self.crop
            )
            # There will be fewer than 4 neighbors if the coordinate being
            # examined is on one of the edges. Make sure these are counted.
            ret += 4 - len(neighbors)

        return ret

    @property
    def sides(self) -> int:
        '''
        Return the number of sides that the region has
        '''
        # Type hints
        Direction = XY

        corners: set[tuple[XY, Direction]] = set()

        # Side detection is done by finding a turn, then walking along that
        # direction until doing so will result in leaving the plot. When that
        # point is found, we've reached the end of a side. Track the sides by
        # tracking corners, represented by a combination of a coordinate and
        # the direction that was walked along a given side.
        plot: XY
        forward: Direction
        for plot in self.plots:
            for forward in self.parent.directions:
                if self.parent.tuple_add(plot, forward) in self.plots:
                    # If you can move in the same direction and not leave the
                    # Region, then this is not a corner. Skip and try the next
                    # direction.
                    continue

                # If we reached here, then we can't move forward without
                # exiting the plot. To turn, reverse the row and column deltas
                # and attempt to walk in that direction. These reverse
                # coordinates are as follows:
                #
                #   1. north -> west    ↱
                #   2. west -> north    ⬑
                #   3. south -> east    ↳
                #   4. east -> south    ⬏
                #
                # Checking these four combinations will account for all
                # possible corners. We don't want to try all combinations of
                # turns, because then we will over-count our sides/corners. I
                # learned this the hard way. 💀
                ptr: XY = plot
                turned: XY = tuple(reversed(forward))
                # Turn and walk in the new direction until it is no longer
                # possible. It is possible as long as both of the following are
                # true:
                #
                #   1. Moving in the new direction does not leave the plot.
                #   2. Moving in the original direction does not stay in the
                #      plot. Remember, the continue statement above ensures
                #      that if the code flow reaches this point, it is no
                #      longer possible to move in the original direction.
                while (
                    self.parent.tuple_add(ptr, turned) in self.plots
                    and self.parent.tuple_add(ptr, forward) not in self.plots
                ):
                    ptr = self.parent.tuple_add(ptr, turned)

                corners.add((ptr, turned))

        return len(corners)

    @property
    def price(self) -> int:
        '''
        The price of the Region, equal to its area times its perimeter
        '''
        return self.area * self.perimeter

    @property
    def discount_price(self) -> int:
        '''
        The price of the Region, factoring in the bulk discount. Equal to the
        area times the number of sides.
        '''
        return self.area * self.sides


class Farm(Grid):
    '''
    Simulates the Farm from the puzzle input
    '''
    @property
    def regions(self) -> Iterator[Region]:
        '''
        Return all the distinct regions in the Farm, using a flood fill
        '''
        # Get all the coordinates in the grid
        remaining_plots: set[XY] = {x[0] for x in self.tile_iter()}

        def flood_fill(coord: XY, visited: Region | None = None) -> Region:
            '''
            Use the flood fill algorithm to find a continuous region containing
            the specified coordinate.
            '''
            visited = visited or set()

            if coord not in visited:
                visited.add(coord)
                crop: str = self[coord]
                neighbor: XY
                neighbor_crop: str
                for neighbor, neighbor_crop in self.neighbors(coord):
                    if crop == neighbor_crop:
                        flood_fill(neighbor, visited)

            return Region(frozenset(visited), self)

        while remaining_plots:
            # Get a coordinate from what remains and use flood fill to get a
            # Region object encompassing all the contiguous matching plots
            region: Region = flood_fill(next(iter(remaining_plots)))  # pylint: disable=stop-iteration-return
            # Exclude this Region's plots from the remaining ones
            remaining_plots -= region.plots
            # Yield the Region object. Once control returns to this generator,
            # repeat the above process until there are no more coordinates
            # remaining in the grid.
            yield region


class AOC2024Day12(AOC):
    '''
    Day 12 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        RRRRIICCFF
        RRRRIICCCF
        VVRRRCCFFF
        VVRCCCJFFF
        VVVVCJJCFE
        VVIVCCJJEE
        VVIIICJJEE
        MIIIIIJJEE
        MIIISIJEEE
        MMMISSJEEE
        '''
    )

    validate_part1: int = 1930
    validate_part2: int = 1206

    # Set by post_init
    farm = None

    def post_init(self) -> None:
        '''
        Load the puzzle input
        '''
        self.farm: Farm = Farm(self.input)

    def part1(self) -> int:
        '''
        Return the sum of all the Regions' prices
        '''
        return sum(x.price for x in self.farm.regions)

    def part2(self) -> int:
        '''
        Return the sum of all the Regions' prices, taking into account the bulk
        discount from Part 2
        '''
        return sum(x.discount_price for x in self.farm.regions)


if __name__ == '__main__':
    aoc = AOC2024Day12()
    aoc.run()
