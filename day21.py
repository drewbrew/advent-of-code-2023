"""Day 21: step counter"""
import heapq
from pathlib import Path


TEST_INPUT = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

REAL_INPUT = Path("day21.txt").read_text()


def parse_input(
    puzzle: str,
) -> tuple[dict[tuple[int, int], str], tuple[int, int]]:
    grid = {}
    start = None
    for y, row in enumerate(puzzle.splitlines()):
        for x, char in enumerate(row):
            if char == "S":
                grid[x, y] = "."
                start = (x, y)
            else:
                grid[x, y] = char
    return grid, start


def part1(puzzle: str, number_of_steps: int = 64) -> int:
    grid, (x, y) = parse_input(puzzle)
    last_steps_taken = 0
    spots_seen_this_round = set()
    queue = [
        (0, (x, y)),
    ]
    heapq.heapify(queue)
    while True:
        last_steps, (x, y) = heapq.heappop(queue)
        if last_steps == number_of_steps:
            # this is our first time at the target
            # since we've filtered for dupes, we should be
            # good to just return the size of the queue at
            # this point but have to include the 1 we just
            # popped
            return len(queue) + 1
        if last_steps != last_steps_taken:
            # reset
            last_steps_taken = last_steps
            spots_seen_this_round = set()
            print(f"now at {last_steps}, queue size {len(queue)}")
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x1 = x + dx
            y1 = y + dy
            if (x1, y1) not in spots_seen_this_round and grid.get(
                (x1, y1),
            ) == ".":
                heapq.heappush(queue, (last_steps + 1, (x1, y1)))
                spots_seen_this_round.add((x1, y1))


def part2(puzzle: str, number_of_steps: int = 26501365) -> int:
    max_x = len(puzzle.splitlines())
    # essentially we find our place at these 3 magic points (my puzzle
    # has length 131, so YMMV)
    after_65, after_196, after_327 = part_2_internal(puzzle, max_x * 3)
    n = number_of_steps // max_x
    # and extrapolate
    return after_65 + n * (
        after_196
        - after_65
        + (n - 1) * (after_327 - after_196 - after_196 + after_65) // 2
    )


def part_2_internal(puzzle: str, number_of_steps: int) -> list[int]:
    grid, (x, y) = parse_input(puzzle)
    max_x, max_y = max(grid)
    max_x += 1
    max_y += 1
    last_steps_taken = 0
    spots_seen_this_round = set()
    done: list[int] = []
    queue = [
        (0, (x, y)),
    ]
    heapq.heapify(queue)
    while True:
        last_steps, (x, y) = heapq.heappop(queue)

        if last_steps == number_of_steps:
            return done
        if last_steps != last_steps_taken:
            # reset
            if last_steps % max_x == 65:
                # save our progress
                done.append(len(queue) + 1)
                print("saved!", done)
                if len(done) == 3:
                    return done
            last_steps_taken = last_steps
            spots_seen_this_round = set()
            print(f"now at {last_steps}, queue size {len(queue)}")

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x1 = x + dx
            y1 = y + dy
            if (x1, y1) not in spots_seen_this_round and grid.get(
                (x1 % max_x, y1 % max_y)
            ) == ".":
                heapq.heappush(queue, (last_steps + 1, (x1, y1)))
                spots_seen_this_round.add((x1, y1))


def main():
    part_1_result = part1(TEST_INPUT, 6)
    assert part_1_result == 16, part_1_result
    print(part1(REAL_INPUT))

    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
