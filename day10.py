from pathlib import Path

import networkx

TEST_INPUT = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

REAL_INPUT = Path("day10.txt").read_text()


def parse_input(puzzle: str) -> tuple[tuple[int, int], networkx.Graph]:
    start = ()
    grid = networkx.Graph()
    lines = puzzle.splitlines()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            # for each character, if the character adjacent to that
            # spot is a valid conection (e.g. a | connects upward to a 7),
            # add that edge to the graph
            # print(x, y, char)
            match char:
                case "S":
                    # print("start")
                    start = (x, y)
                case "|":
                    # vertical
                    # down needs to have a vertical part upwards
                    try:
                        if lines[y + 1][x] in "|LJS":
                            # print("adding down")
                            grid.add_edge((x, y), (x, y + 1))
                    except IndexError:
                        pass
                    # up needs to have a vertical part downwards
                    try:
                        if lines[y - 1][x] in "|7FS":
                            # print("adding up")
                            grid.add_edge((x, y), (x, y - 1))
                    except IndexError:
                        pass
                case "-":
                    # horizontal
                    # right needs to connect to west
                    try:
                        if lines[y][x + 1] in "S-J7":
                            # print("adding right")
                            grid.add_edge((x, y), (x + 1, y))
                    except IndexError:
                        pass
                    # left needs to connect to east
                    try:
                        if lines[y][x - 1] in "S-FL":
                            # print("adding left")
                            grid.add_edge((x, y), (x - 1, y))
                    except IndexError:
                        pass
                case "L":
                    # connects N and E
                    # up needs to have a vertical part downwards
                    try:
                        if lines[y - 1][x] in "|7FS":
                            # print("adding up")
                            grid.add_edge((x, y), (x, y - 1))
                    except IndexError:
                        pass
                    # right needs to connect to west
                    try:
                        if lines[y][x + 1] in "S-J7":
                            # print("adding right")
                            grid.add_edge((x, y), (x + 1, y))
                    except IndexError:
                        pass
                case "J":
                    # connects N and W
                    # up needs to have a vertical part downwards
                    try:
                        if lines[y - 1][x] in "|7FS":
                            # print("adding up")
                            grid.add_edge((x, y), (x, y - 1))
                    except IndexError:
                        pass
                    # left needs to connect to east
                    try:
                        if lines[y][x - 1] in "S-FL":
                            # print("adding left")
                            grid.add_edge((x, y), (x - 1, y))
                    except IndexError:
                        pass
                case "7":
                    # S and W
                    # down needs to have a vertical part upwards
                    try:
                        if lines[y + 1][x] in "|LJS":
                            # print("adding down")
                            grid.add_edge((x, y), (x, y + 1))
                    except IndexError:
                        pass
                    # left needs to connect to east
                    try:
                        if lines[y][x - 1] in "S-FL":
                            # print("adding left")
                            grid.add_edge((x, y), (x - 1, y))
                    except IndexError:
                        pass
                case "F":
                    # print("SE")
                    # S and E
                    # down needs to have a vertical part upwards
                    try:
                        if lines[y + 1][x] in "|LJS":
                            # print("adding down")
                            grid.add_edge((x, y), (x, y + 1))
                    except IndexError:
                        # print("narp", (x, y + 1))
                        pass
                    # right needs to connect to west
                    try:
                        if lines[y][x + 1] in "S-J7":
                            # print("adding right")
                            grid.add_edge((x, y), (x + 1, y))
                    except IndexError:
                        pass
                case ".":
                    # ground
                    pass
                case _:
                    raise ValueError(f"Unknown character {char}")
    return start, grid


def part1(puzzle: str) -> int:
    start, grid = parse_input(puzzle)
    max_dist = 0
    for x, y in grid.nodes:
        # print(x, y)
        try:
            if (
                length := networkx.shortest_path_length(
                    grid,
                    start,
                    (x, y),
                )
            ) > max_dist:
                print(f"path from {start} to {x, y} is {length}")
                max_dist = length
        except networkx.exception.NetworkXNoPath:
            pass

    return max_dist


def part2(puzzle: str) -> int:
    start, grid = parse_input(puzzle)
    start_trips = [edge for edge in grid.edges if start in edge]
    assert len(start_trips) == 2, start_trips
    last_stop = start_trips[-1]
    other_dest = [coord for coord in last_stop if coord != start][0]
    grid.remove_edge(*last_stop)
    path_back = networkx.shortest_path(grid, start, other_dest)
    main_loop = set(path_back)
    main_loop.add(start)
    insiders = 0
    for y, line in enumerate(puzzle.splitlines()):
        # print(y, insiders)
        for x in range(len(line)):
            if (x, y) not in main_loop:
                verts_seen = 0
                for dx in range(x):
                    # note: visual inspection revealed my start piece is a J
                    # effectively, we need to see how many times parity has
                    # changed by looking at upward bends and pipes
                    if (dx, y) in main_loop and line[dx] in "|JLS":
                        verts_seen += 1
                if verts_seen % 2 == 1:
                    insiders += 1
    return insiders


def main():
    part_1_test = part1(TEST_INPUT)
    assert part_1_test == 8, part_1_test
    print(part1(REAL_INPUT))
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
