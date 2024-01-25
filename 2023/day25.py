#!/usr/bin/env python
'''
https://adventofcode.com/2023/day/25
'''
from __future__ import annotations
import copy
import itertools
import math
import random
import sys
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field

# Local imports
from aoc import AOC


@dataclass
class Edge:
    '''
    Represents a single edge from the graph
    '''
    u: str
    v: str
    orig_u: str = field(init=False)
    orig_v: str = field(init=False)

    def __post_init__(self) -> None:
        '''
        Assign original values so we can track what wires need to be cut
        '''
        self.orig_u = self.u
        self.orig_v = self.v

    @property
    def is_loop(self) -> bool:
        '''
        Returns true if u and v are the same node (i.e. the edge connects to
        itself).
        '''
        return self.u == self.v

    def __hash__(self) -> int:
        '''
        Allow sets to treat instances with inverse u/v values as the same
        '''
        return hash(frozenset({self.u, self.v}))

    def __eq__(self, other: Edge) -> bool:
        '''
        Define equality as the same two u/v values, irrespective of which is
        assigned to which.
        '''
        return hash(self) == hash(other)

    def replace(self, old: str, new: str) -> None:
        '''
        Replace old node name with new one
        '''
        if self.u == old:
            self.u = new
        elif self.v == old:
            self.v = new
        else:
            raise ValueError(f'{self} has no node {old!r}')


class ComponentGraph:
    '''
    Represents the connectivities described by the puzzle input as a
    connected graph.
    '''
    def __init__(self, data: str):
        '''
        Load the input file
        '''
        node_connections: defaultdict[set[str]] = defaultdict(set)

        for line in data.splitlines():
            cols: list[str] = line.replace(':', '').split()
            node: str = cols[0]
            connections: list[str] = cols[1:]
            node_connections[node].update(connections)
            connection: str
            for connection in connections:
                node_connections[connection].add(node)

        # Use the Edge dataclass' hash function to disambiguate edges which are
        # inverse of each other, resulting in a list of distinct edges.
        self.edges: list[Edge] = list(
            set(
                itertools.chain.from_iterable(
                    (
                        (
                            Edge(node, connection)
                            for connection in connections
                        ) for node, connections in node_connections.items()
                    )
                )
            )
        )

    def karger(self) -> tuple[tuple[int, int], tuple[Edge, ...]]:
        '''
        The puzzle describes the system of connections defined by the puzzle
        input as a K-connected graph, where K=3.

        Knowing this, we can run Karger's Algorithm repeatedly until it
        produces two supernodes, both of which have 3 edges. We already know
        the mincut, so there is no need to run the algorithm a large number of
        times and take the run with the fewest number of edges.

        Return a tuple of the cardinality of each supernode (i.e. the size of
        each group), and another tuple of Edge objects representing the wires
        one would need to cut to disconnect the graph.
        '''
        while True:
            # Get a random order of our collection of edges
            edges = copy.deepcopy(self.edges)
            random.shuffle(edges)

            nodes = defaultdict(list)

            for edge in edges:
                nodes[edge.u].append(edge)
                nodes[edge.v].append(edge)

            # To start, each node only represents a single member (i.e. none
            # of them have been contracted into supernodes). As we contract
            # nodes we will create (or add to) supernodes. The cardinality of a
            # given supernode will be equal to the number of its members.
            cardinality: dict[str, int] = {node: 1 for node in nodes}

            while len(nodes) > 2:
                edge = edges.pop()
                u, v = edge.u, edge.v

                if edge.is_loop:
                    # Ignore any Edges that were turned into self-loops in a
                    # prior iteration
                    continue

                # Contract v into u
                for edge in nodes.pop(v):
                    try:
                        edge.replace(v, u)
                    except ValueError:
                        pass
                    nodes[u].append(edge)

                # With v's edges collapsed into the supernode u, u gains the
                # cardinality of the node/supernode v.
                cardinality[u] += cardinality.pop(v)

                # Prune self edges created for node u in this loop iteration
                nodes[u] = [e for e in nodes[u] if not e.is_loop]

            # After contracting the nodes dict down to two keys, it will
            # represent the 2 supernodes. Both keys' values will contain the
            # same exact Edge objects (albeit not necessarily in the same
            # order). These Edge objects represent the wires one would need to
            # cut to separate the supernodes from each other. Over the course
            # of the contractions, the u/v values for each remaining Edge will
            # have been overwritten, but the original u/v values are held in
            # the object's "orig_u" and "orig_v" entries.

            # Get the name of one of the supernodes (doesn't matter which, they
            # both have the same Edges)
            name: str = next(iter(nodes))
            # The number of the Edges == the number of wires connecting the two
            # supernodes.
            num_wires: int = len(nodes[name])

            if num_wires == 3:
                return tuple(cardinality.values()), tuple(nodes[name])


class AOC2023Day25(AOC):
    '''
    Day 25 of Advent of Code 2023
    '''
    example_data: str = textwrap.dedent(
        '''
        jqt: rhn xhk nvd
        rsh: frs pzl lsr
        xhk: hfx
        cmg: qnr nvd lhk bvb
        rhn: xhk bvb hfx
        bvb: xhk hfx
        pzl: lsr hfx nvd
        qnr: nvd
        ntq: jqt hfx bvb xhk
        nvd: lhk
        lsr: lhk
        rzs: qnr cmg lsr rsh
        frs: qnr lhk lsr
        '''
    )

    validate_part1: int = 54

    def part1(self) -> int:
        '''
        Use Karger's Algorithm to find the exact wires to cut in order to
        separate the nodes into two distinct groups.
        '''
        graph: ComponentGraph = ComponentGraph(self.input)
        cardinalities: tuple[int, int]
        wires: tuple[Edge]

        cardinalities, wires = graph.karger()

        if not self.example:
            for wire in wires:
                sys.stdout.write(f'Cut wire {wire.orig_u}/{wire.orig_v}\n')
            sys.stdout.write('\n')

        return math.prod(cardinalities)


if __name__ == '__main__':
    aoc = AOC2023Day25()
    aoc.run()
