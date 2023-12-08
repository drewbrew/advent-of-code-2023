from itertools import cycle
from math import lcm
from pathlib import Path


TEST_INPUT_1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

TEST_INPUT_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

PART_2_TEST_INPUT = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

REAL_INPUT = Path("day08.txt").read_text()


def part1(puzzle_input: str) -> int:
    steps, nodes = puzzle_input.split("\n\n")
    directions = {}
    for line in nodes.splitlines():
        source, target = line.split(" = ")
        left, right = target[1:-1].split(", ")
        directions[source] = (left, right)
    location = "AAA"
    instructions = cycle(steps)
    steps_taken = 0
    while location != "ZZZ":
        left, right = directions[location]
        movement = next(instructions)
        if movement == "L":
            location = left
        else:
            location = right
        steps_taken += 1
    return steps_taken


def part2(puzzle_input: str) -> int:
    steps, nodes = puzzle_input.split("\n\n")
    directions = {}
    for line in nodes.splitlines():
        source, target = line.split(" = ")
        left, right = target[1:-1].split(", ")
        directions[source] = (left, right)
    locations = [loc for loc in directions if loc.endswith("A")]
    instructions = cycle(steps)
    steps_taken = 0
    hits = {}
    # print("locations", locations)
    while not all(loc.endswith("Z") for loc in locations):
        if len(hits) == len(locations):
            # print("Found repeats:", hits)
            return lcm(*hits.values())
        new_locations = []
        movement = next(instructions)
        for location in locations:
            left, right = directions[location]

            if movement == "L":
                location = left
            else:
                location = right
            if location.endswith("Z"):
                print(
                    f"move {steps_taken + 1}: location "
                    f"{len(new_locations)} is at {location}"
                )
                if len(new_locations) not in hits:
                    hits[len(new_locations)] = steps_taken + 1
            new_locations.append(location)
        locations = new_locations
        steps_taken += 1

    return steps_taken


def main():
    part_1_short = part1(TEST_INPUT_1)
    assert part_1_short == 2, part_1_short
    part_1_long = part1(TEST_INPUT_2)
    assert part_1_long == 6, part_1_long
    print(part1(REAL_INPUT))
    part_2_test = part2(PART_2_TEST_INPUT)
    assert part_2_test == 6, part_2_test
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
