"""Day 6: a day at the (really short) boat races"""

from pathlib import Path

TEST_INPUT = """Time:      7  15   30
Distance:  9  40  200"""

REAL_INPUT = Path("day06.txt").read_text()


def part1(puzzle_input: str) -> int:
    score = 1
    time, distance = puzzle_input.splitlines()
    times = [int(i) for i in time.split(":")[1].split()]
    distances = [int(i) for i in distance.split(":")[1].split()]
    for t, d in zip(times, distances):
        possible_ways = sum(
            int((t - hold_time) * hold_time > d) for hold_time in range(1, t)
        )
        score *= possible_ways
    return score


def part2(puzzle_input: str) -> int:
    score = 1
    time, distance = puzzle_input.splitlines()
    t = int(time.split(":")[1].replace(" ", ""))
    d = int(distance.split(":")[1].replace(" ", ""))

    possible_ways = sum(
        int((t - hold_time) * hold_time > d) for hold_time in range(1, t)
    )
    score *= possible_ways
    return score


def main():
    part_1_score = part1(TEST_INPUT)
    assert part_1_score == 288, part_1_score
    print(part1(REAL_INPUT))
    part_2_score = part2(TEST_INPUT)
    assert part_2_score == 71503, part_2_score
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
