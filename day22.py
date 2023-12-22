"""Day 22: sand slabs"""

from pathlib import Path

import networkx


TEST_INPUT = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

REAL_INPUT = Path("day22.txt").read_text()


def parse_input(puzzle: str) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    """Convert the puzzle into a list of 3D blocks"""
    blocks = []
    for line in puzzle.splitlines():
        a, b = line.split("~")
        blocks.append(
            (
                tuple(int(i) for i in a.split(",")),
                tuple(int(i) for i in b.split(",")),
            )
        )
    return blocks


def part1(puzzle: str) -> tuple[int, int]:
    blocks = parse_input(puzzle=puzzle)
    blocks = sorted(blocks, key=lambda block: min(block[0][2], block[1][2]))
    for (x1, y1, z1), (x2, y2, z2) in blocks:
        # make sure all the blocks are flat in two dimensions
        assert (x1 == x2 and (y1 == y2 or z1 == z2)) or (y1 == y2 and z1 == z2), (
            x1,
            y1,
            z1,
            x2,
            y2,
            z2,
        )
    base_setup = make_fall(blocks)
    base_setup = sorted(base_setup, key=lambda block: min(block[0][2], block[1][2]))
    print("\n".join(str(i) for i in base_setup))
    unaffected = 0
    chain_reactions = 0
    graph = networkx.DiGraph()
    for index, block in enumerate(base_setup):
        if block[0][2] == 1 or block[1][2] == 1:
            graph.add_edge(block, "ground")
        else:
            # find all the blocks
            xmin, xmax = sorted(x for x, _, _ in block)
            x_range = set(range(xmin, xmax + 1))
            ymin, ymax = sorted(y for _, y, _ in block)
            y_range = set(range(ymin, ymax + 1))
            for (x, y, z), (x1, y1, z1) in base_setup[:index]:
                if (
                    z != block[0][2] - 1
                    and z != block[1][2] - 1
                    and z1 != block[0][2] - 1
                    and z1 != block[1][2]
                ):
                    # not 1 level down, can't continue
                    continue
                x1min, x1max = sorted([x, x1])
                y1min, y1max = sorted([y, y1])
                if x_range & set(range(x1min, x1max + 1)) and y_range & set(
                    range(y1min, y1max + 1)
                ):
                    graph.add_edge(block, ((x, y, z), (x1, y1, z1)))
    # print(graph.nodes)
    for index, block in enumerate(base_setup):
        inner_reactions = 0
        new_graph = graph.copy()
        new_graph.remove_node(block)
        for other_block in base_setup[index + 1 :]:
            if not networkx.has_path(new_graph, other_block, "ground"):
                inner_reactions += 1
        if inner_reactions:
            # print(f"{blocks[index]}, {inner_reactions}, {chain_reactions}")
            chain_reactions += inner_reactions
        else:
            # print(f"{blocks[index]} nope {chain_reactions}")
            unaffected += 1
    return unaffected, chain_reactions


def make_fall(
    blocks: list[tuple[tuple[int, int, int], tuple[int, int, int]]]
) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    """Make the blocks fall!"""
    occupied_blocks: set[tuple[int, int, int]] = set()
    new_blocks = []
    for block in sorted(blocks, key=lambda block: min(block[0][2], block[1][2])):
        # print("working on block", block)
        (x1, y1, z1), (x2, y2, z2) = block
        dz1 = z1
        dz2 = z2
        while min(dz1, dz2) > 1:
            dz1 = z1 - 1
            dz2 = z2 - 1
            if x1 >= x2:
                x_range = range(x2, x1 + 1)
            else:
                x_range = range(x1, x2 + 1)
            if y1 >= y2:
                y_range = range(y2, y1 + 1)
            else:
                y_range = range(y1, y2 + 1)
            if z1 >= z2:
                z_range = range(dz2, dz1 + 1)
            else:
                z_range = range(dz1, dz2 + 1)
            if set(
                (ax, ay, az) for ax in x_range for ay in y_range for az in z_range
            ).intersection(occupied_blocks):
                # can't fall!
                break
            z1 = dz1
            z2 = dz2
        new_blocks.append(((x1, y1, z1), (x2, y2, z2)))
        # print("fell to", new_blocks[-1])
        if x1 >= x2:
            x_range = range(x2, x1 + 1)
        else:
            x_range = range(x1, x2 + 1)
        if y1 >= y2:
            y_range = range(y2, y1 + 1)
        else:
            y_range = range(y1, y2 + 1)
        if z1 >= z2:
            z_range = range(z2, z1 + 1)
        else:
            z_range = range(z1, z2 + 1)
        occupied = set(
            (ax, ay, az) for ax in x_range for ay in y_range for az in z_range
        )
        occupied_blocks |= occupied
    return new_blocks


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == (5, 7), part_1_result
    print(part1(REAL_INPUT))


if __name__ == "__main__":
    main()
