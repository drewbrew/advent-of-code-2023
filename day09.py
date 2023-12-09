"""Day 9: mirage maintenance"""

from pathlib import Path

TEST_INPUT = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

REAL_INPUT = Path("day09.txt").read_text()


def history_with_next_step(history: list[int]) -> list[int]:
    """Find the next value of a sequence using extrapolation"""
    # print("a", history)
    next_step = dxes(history)
    # print("b", next_step)
    if len(set(next_step)) == 1:
        # print("done", history, history[-1], history[-2])
        return history + [history[-1] + (history[-1] - history[-2])]
    recursed = history_with_next_step(next_step)
    # print("recursion result", recursed)
    assert len(recursed) == len(history), (recursed, history)
    return history + [history[-1] + recursed[-1]]


def history_with_previous_step(history: list[int]) -> list[int]:
    """Find the previous value of a sequence using extrapolation"""
    # print("a", history)
    next_step = dxes(history)
    # print("b", next_step)
    if len(set(next_step)) == 1:
        # print("done", history, history[-1], history[-2])
        return [history[0] - (history[1] - history[0])] + history
    recursed = history_with_previous_step(next_step)
    # print("recursion result", recursed)
    assert len(recursed) == len(history), (recursed, history)
    end = [history[0] - recursed[0]] + history
    # print("returning", end)
    return end


def dxes(history: list[int]) -> list[int]:
    """Keep working down the dx tree until we get all zeroes
    >>> dxes([0, 3, 6, 9, 12, 15])
    [3, 3, 3, 3, 3]

    >>> dxes([1, 3, 6, 10, 15, 21, 28])
    [2, 3, 4, 5, 6, 7]
    """

    return [dx - x for (x, dx) in zip(history[:-1], history[1:])]


def part1(puzzle_input: str) -> int:
    lines = []
    for line in puzzle_input.splitlines():
        lines.append([int(num) for num in line.split()])
    new_lines = [history_with_next_step(line) for line in lines]
    return sum(line[-1] for line in new_lines)


def part2(puzzle_input: str) -> int:
    lines = []
    for line in puzzle_input.splitlines():
        lines.append([int(num) for num in line.split()])
    new_lines = [history_with_previous_step(line) for line in lines]
    return sum(line[0] for line in new_lines)


def main():
    assert history_with_next_step([1, 3, 6, 10, 15, 21]) == [
        1,
        3,
        6,
        10,
        15,
        21,
        28,
    ], history_with_next_step([1, 3, 6, 10, 15, 21])
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 114, part_1_result
    print(part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 2, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
