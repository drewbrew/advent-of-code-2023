"""Day 25: cut the wires!"""

from pathlib import Path
from itertools import combinations

import networkx

TEST_INPUT = """jqt: rhn xhk nvd
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
frs: qnr lhk lsr"""


REAL_INPUT = Path("day25.txt").read_text()


def parse_input(puzzle: str) -> networkx.Graph:
    graph = networkx.Graph()
    for line in puzzle.splitlines():
        source, targets = line.split(": ")
        for target in targets.split():
            graph.add_edge(source, target)
    return graph


def graph_to_dot(graph: networkx.Graph) -> str:
    output = ["graph {"]
    for node1, node2 in graph.edges:
        output.append(f"    {node1} -- {node2}")
    output.append("}")
    return "\n".join(output)


def part1(puzzle: str) -> None:
    graph = parse_input(puzzle=puzzle)
    rendered = graph_to_dot(graph=graph)
    dotfile = Path(f'day25{"test" if puzzle == TEST_INPUT else ""}.dot')
    dotfile.write_text(rendered)
    print(f'Now run neato -Tsvg {dotfile.name} > {dotfile.name.replace("dot", "svg")}')
    print("then look at the graph to find the critical links")
    print("Come back here and edit the code to replace the definitions of the three")
    print("edges below")
    edge1 = ("bff", "rhk")
    edge2 = ("qpp", "vnm")
    edge3 = ("kfr", "vkp")
    iterable = graph.edges if puzzle == TEST_INPUT else [edge1, edge2, edge3]
    for edge1, edge2, edge3 in combinations(iterable, 3):
        new_graph = graph.copy()
        new_graph.remove_edge(*edge1)
        new_graph.remove_edge(*edge2)
        new_graph.remove_edge(*edge3)
        sets_seen = set()
        for node in new_graph.nodes:
            neighbors = tuple(
                sorted(networkx.node_connected_component(new_graph, node))
            )
            sets_seen.add(neighbors)
        # print(f"removed {edge1}, {edge2}, {edge3}; got {[len(i) for i in sets_seen]}")
        if len(sets_seen) == 2:
            a, b = list(sets_seen)
            print(f"removed {edge1}, {edge2}, {edge3} and got {len(a)} and {len(b)}")
            return len(a) * len(b)
    raise ValueError("did not work")


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 54, part_1_result
    print(part1(REAL_INPUT))


if __name__ == "__main__":
    main()
