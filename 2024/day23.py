#!/usr/bin/env python
'''
https://adventofcode.com/2024/day/23
'''
import textwrap
from collections import defaultdict
from collections.abc import Iterator

# Local imports
from aoc import AOC

# Type hints
Vertex = str
Clique = frozenset[Vertex] | set[Vertex]
Neighbors = frozenset[Vertex]


class AOC2024Day23(AOC):
    '''
    Day 23 of Advent of Code 2024
    '''
    example_data: str = textwrap.dedent(
        '''
        kh-tc
        qp-kh
        de-cg
        ka-co
        yn-aq
        qp-ub
        cg-tb
        vc-aq
        tb-ka
        wh-tc
        yn-cg
        kh-ub
        ta-co
        de-co
        tc-td
        tb-wq
        wh-td
        ta-ka
        td-qp
        aq-cg
        wq-ub
        ub-vc
        de-ta
        wq-aq
        wq-vc
        wh-yn
        ka-de
        kh-ta
        co-tc
        wh-qp
        tb-vc
        td-yn
        '''
    )

    validate_part1: int = 7
    validate_part2: str = 'co,de,ka,ta'

    # Set by post_init
    graph = None

    def post_init(self) -> None:
        '''
        Load the input into a Maze object
        '''
        graph: defaultdict[set[Vertex]] = defaultdict(set)
        first: Vertex
        second: Vertex
        for first, second in (
            line.split('-') for line in self.input.splitlines()
        ):
            graph[first].add(second)
            graph[second].add(first)

        # Freeze the graph
        self.graph: dict[Vertex, Neighbors] = {
            x: frozenset(y) for x, y in graph.items()
        }

    def bron_kerbosch(
        self,
        R: set[Vertex],
        P: set[Vertex],
        X: set[Vertex],
    ) -> Iterator[Clique]:
        r'''
        Pseudocode from Wikipedia:

        https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm#With_pivoting

        algorithm BronKerbosch2(R, P, X) is
            if P and X are both empty then
                report R as a maximal clique
            choose a pivot vertex u in P ⋃ X
            for each vertex v in P \ N(u) do
                BronKerbosch2(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
                P := P \ {v}
                X := X ⋃ {v}
        '''
        if not P and not X:
            yield R
        else:
            # Find the vertex in either P or X which has the largest number of
            # connections, and choose that as the pivot vertex
            pivot_vertex = max(P.union(X), key=lambda node: len(self.graph[node]))
            for vertex in P - self.graph[pivot_vertex]:
                yield from self.bron_kerbosch(
                    R.union({vertex}),
                    P.intersection(self.graph[vertex]),
                    X.intersection(self.graph[vertex]),
                )
                P.remove(vertex)
                X.add(vertex)

    def part1(self) -> int:
        '''
        Return the number of 3-vertex cliques with at least one member starting
        in the letter "t"
        '''
        cliques: set[Clique] = set()

        # Get the iteration order
        nodes: tuple[Vertex, ...] = tuple(self.graph)

        # self.graph contains each Vertex mapped to a set of its connections.
        # By performing a nested offset loop over the graph in the same
        # iteration order, we can reduce the search space, because as we
        # proceed through these iterations, we will have already checked all
        # the possible connections for the prior entries.
        #
        # To begin, iterate over the vertexes in the graph. This iteration
        # order will be the same as the "nodes" tuple we created above.
        index: int
        first: Vertex
        second: Vertex
        third: Vertex
        for index, first in enumerate(self.graph):
            # Loop over all connections that the current Vertex has. For each
            # "second" node, we have 2/3 of a 3-node clique.
            for second in self.graph[first]:
                # If the next index in the iteration order contains connections
                # for both the first and second nodes (i.e. is a superset of
                # those two), then we have found a 3-node clique.
                for third in nodes[index + 1:]:
                    if (
                        self.graph[third].issuperset({first, second})
                        and any(x.startswith('t') for x in (first, second, third))
                    ):
                        # Only add a clique if one of vts vertexes starts with "t"
                        cliques.add(frozenset({first, second, third}))

        return len(cliques)

    def part2(self) -> str:
        '''
        Return the largest clique, sorted and joined by commas, using the
        Bron-Kerbosch Algorithm.
        '''
        return ','.join(
            sorted(
                max(
                    self.bron_kerbosch(set(), set(self.graph), set()),
                    key=len
                )
            )
        )


if __name__ == '__main__':
    aoc = AOC2024Day23()
    aoc.run()
