"""Day 23: let's go for a hike"""

from pathlib import Path

import networkx

TEST_INPUT = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

REAL_INPUT = Path("day23.txt").read_text()


def parse_input(
    puzzle: str,
) -> tuple[networkx.DiGraph, tuple[int, int], tuple[int, int]]:
    graph = networkx.DiGraph()
    lines = puzzle.splitlines()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == ".":
                last_pos = (x, y)
                if not y:
                    start = last_pos
                for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                    try:
                        neighbor = lines[y + dy][x + dx]
                    except IndexError:
                        continue
                    if neighbor == ".":
                        # add edges in both directions
                        graph.add_edge(
                            (x, y),
                            (x + dx, y + dy),
                        )
                        graph.add_edge(
                            (x, y),
                            (x + dx, y + dy),
                        )
                    elif neighbor in "<>^v":
                        # it's a slope
                        # only add the inbound connection
                        # we'll deal with the outbound connection below
                        invalid_step = {
                            ">": (-1, 0),  # can't walk uphill
                            "<": (1, 0),
                            "^": (0, 1),
                            "v": (0, -1),
                        }[neighbor]
                        if (dx, dy) != invalid_step:
                            graph.add_edge(
                                (x, y),
                                (x + dx, y + dy),
                            )
            elif char in "^>v<":
                dx, dy = {
                    ">": (1, 0),
                    "<": (-1, 0),
                    "v": (0, 1),
                    "^": (0, -1),
                }[char]
                assert lines[y + dy][x + dx] in "^.<>v"
                graph.add_edge(
                    (x, y),
                    (x + dx, y + dy),
                )

    return graph, start, last_pos


def part1(puzzle: str) -> int:
    """Find the longest path from start to end that doesn't involve backtracking"""
    grid, start, end = parse_input(puzzle=puzzle)
    paths = networkx.all_simple_paths(grid, start, end)
    lengths = [len(path) for path in paths]
    print(lengths)
    return max(lengths) - 1  # networkx includes an extra step on each path


def parse_input_p2(
    puzzle: str,
) -> tuple[networkx.Graph, tuple[int, int], tuple[int, int]]:
    graph = networkx.Graph()
    lines = puzzle.splitlines()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char in ".<>v^":
                last_pos = (x, y)
                if not y:
                    start = last_pos
                for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                    try:
                        neighbor = lines[y + dy][x + dx]
                    except IndexError:
                        continue
                    if neighbor in "<>^v.":
                        graph.add_edge(
                            (x, y),
                            (x + dx, y + dy),
                        )

    return graph, start, last_pos


def part2(puzzle: str) -> int:
    """Find the longest path from start to end that doesn't involve backtracking

    Only this time, ignoring slopes (so extra long)
    """
    grid, start, end = parse_input_p2(puzzle=puzzle)
    paths = networkx.all_simple_paths(grid, start, end)
    max_length = 0
    for path in paths:
        new_length = len(path)
        if new_length > max_length:
            print(new_length, end="\r")
            max_length = new_length
    return max_length - 1  # networkx includes an extra step on each path


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 94, part_1_result
    print(part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 154, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
