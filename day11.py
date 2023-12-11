"""Day 11: Cosmic Expansion"""

from pathlib import Path


TEST_INPUT = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

REAL_INPUT = Path("day11.txt").read_text()


def parse_input(puzzle: str) -> set[tuple[int, int]]:
    vertically_expanded = []
    for line in puzzle.splitlines():
        if all(char == "." for char in line):
            # if we have an entirely blank row, add it twice
            vertically_expanded.append(line[:])
        vertically_expanded.append(line[:])
    # print("\n".join(vertically_expanded))
    horizontally_expanded = [[] for _ in range(len(vertically_expanded))]
    for x in range(len(vertically_expanded[0])):
        if all(char == "." for char in (line[x] for line in vertically_expanded)):
            for row in horizontally_expanded:
                row.append(".")
        for y in range(len(vertically_expanded)):
            horizontally_expanded[y].append(vertically_expanded[y][x])
    # print(horizontally_expanded)
    grid = set()
    for y, row in enumerate(horizontally_expanded):
        for x, char in enumerate(row):
            if char == "#":
                grid.add((x, y))
    return grid


def part1(puzzle_input: str) -> int:
    grid = list(parse_input(puzzle_input))
    # print(grid)
    distances = 0
    for index, (x, y) in enumerate(grid):
        for dx, dy in grid[index + 1 :]:
            distances += abs(dx - x) + abs(dy - y)
    return distances


def parse_input_part_2(puzzle: str) -> tuple[set[tuple[int, int]], set[int], set[int]]:
    grid = set()
    blank_rows = set()
    blank_columns = set()
    lines = puzzle.splitlines()
    for index, line in enumerate(lines):
        if all(char == "." for char in line):
            blank_rows.add(index)
    for x in range(len(lines[0])):
        if all(char == "." for char in (line[x] for line in lines)):
            blank_columns.add(x)
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == "#":
                grid.add((x, y))
    return grid, blank_rows, blank_columns


def part2(puzzle_input: str, growth_factor: int = 1_000_000) -> int:
    grid, blank_rows, blank_columns = parse_input_part_2(puzzle_input)
    grid = list(grid)
    # print(grid, blank_rows, blank_columns)
    distances = 0
    for index, (x, y) in enumerate(grid):
        for dx, dy in grid[index + 1 :]:
            low_x, high_x = sorted([x, dx])
            low_y, high_y = sorted([y, dy])
            blank_rows_hit = blank_rows.intersection(range(low_y, high_y + 1))
            blank_columns_hit = blank_columns.intersection(range(low_x, high_x + 1))
            extra_x = 0
            extra_y = 0
            if blank_rows_hit:
                extra_y = len(blank_rows_hit) * (growth_factor - 1)
            if blank_columns_hit:
                extra_x = len(blank_columns_hit) * (growth_factor - 1)
            dist = (abs(dx - x) + extra_x) + (abs(dy - y) + extra_y)
            # print(
            #     (x, y),
            #     (dx, dy),
            #     dist,
            #     extra_x,
            #     blank_columns_hit,
            #     extra_y,
            #     blank_rows_hit,
            # )
            distances += dist

    return distances


def main():
    test_result = part1(TEST_INPUT)
    assert test_result == 374, test_result
    print(part1(REAL_INPUT))
    part_2_test_result = part2(TEST_INPUT, 10)
    assert part_2_test_result == 1030, part_2_test_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
