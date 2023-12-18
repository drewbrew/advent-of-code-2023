"""Day 18: lavaduct lagoon"""
from collections import Counter
from pathlib import Path

import numpy as np

TEST_INPUT = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

REAL_INPUT = Path("day18.txt").read_text()


def part1(puzzle: str) -> int:
    x = 0
    y = 0
    headings = {
        "R": (1, 0),
        "L": (-1, 0),
        "D": (0, -1),
        "U": (0, 1),
    }
    spots_filled = [(x, y)]
    lines = puzzle.splitlines()
    for line in lines:
        direction, amount, _ = line.split()
        amount = int(amount)
        dx, dy = headings[direction]
        for _ in range(amount):
            x += dx
            y += dy
            spots_filled.append((x, y))

    area_contained = area(spots_filled)
    return len(spots_filled) + (area_contained - len(spots_filled) // 2)


def part2(puzzle: str) -> int:
    x = 0
    y = 0
    headings = {
        "0": (1, 0),  # right
        "2": (-1, 0),  # left
        "1": (0, -1),  # down
        "3": (0, 1),  # up
    }
    spots_filled = [(x, y)]
    lines = puzzle.splitlines()
    number_of_points = 0
    for line in lines:
        instr = line.split()[-1][2:-1]
        assert len(instr) == 6, instr
        direction = instr[-1]
        amount = int(instr[:-1], 16)
        dx, dy = headings[direction]
        # print(dx, dy, amount)

        x += dx * amount
        y += dy * amount
        spots_filled.append((x, y))
        number_of_points += amount
    area_contained = area(spots_filled)
    return area_contained - number_of_points // 2 + number_of_points + 1


# https://stackoverflow.com/a/30408825
def area(vertices: list[tuple[int, int]]):
    x = [i[0] for i in vertices]
    y = [i[1] for i in vertices]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 62, part_1_result
    print(round(part1(REAL_INPUT)))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 952408144115, part_2_result
    print(round(part2(REAL_INPUT)))


if __name__ == "__main__":
    main()
