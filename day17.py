"""Day 17: don't go chasing lavafalls"""
from functools import cache
from time import perf_counter
from pathlib import Path
import heapq

TEST_INPUT = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

PART_2_TEST_INPUT = """111111111111
999999999991
999999999991
999999999991
999999999991"""

REAL_INPUT = Path("day17.txt").read_text()


def parse_input(puzzle: str) -> dict[tuple[int, int], int]:
    grid = {}
    for y, row in enumerate(puzzle.splitlines()):
        for x, char in enumerate(row):
            grid[x, y] = int(char)
    return grid


def part1(puzzle: str) -> int:
    """Find the path with the lowest cost with the caveat that you can't go straight more than 3x"""
    start = (0, 0)
    grid = parse_input(puzzle)
    dest = max(grid)
    max_x, max_y = dest
    assert max_x == max_y  # making this a square
    # print(dest)
    # so, our conditions that we need to track:
    # 1. total cost
    # 2. position
    # 3. last 3 bearings
    last_bearings = []
    total_cost = 0
    paths = [
        (total_cost, start, last_bearings),
    ]
    heapq.heapify(paths)
    lowest_costs = {}
    while paths:
        total_cost, start, last_bearings = heapq.heappop(paths)
        # print(total_cost, start, last_bearings)
        if start == dest:
            # print("I made it!", last_bearings, start)
            return total_cost
        try:
            # have we been here for cheaper?
            lowest_costs[(start, tuple(last_bearings[-3:]))]
        except KeyError:
            lowest_costs[(start, tuple(last_bearings[-3:]))] = total_cost
        else:
            # we already have
            continue
        last_directions = set(last_bearings[-3:])
        valid_turns = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        try:
            last_x, last_y = last_bearings[-1]
            # can't go backwards
            valid_turns.remove(
                (
                    -last_x if last_x else 0,
                    -last_y if last_y else 0,
                )
            )
            # print(f'removed {(-last_x if last_x else 0, -last_y if last_y else 0)}', last_directions)
        except IndexError:
            # first turn
            assert total_cost == 0
        if len(last_directions) > 1 and len(last_directions) == 1:
            # we have to turn
            # print(f'removing {last_x, last_y}')
            valid_turns.remove((last_x, last_y))
        # print(valid_turns)
        x, y = start
        for dx, dy in valid_turns:
            if last_bearings[-3:] == [(dx, dy), (dx, dy), (dx, dy)]:
                # print(f'skipping {dx, dy}')
                continue
            try:
                heapq.heappush(
                    paths,
                    (
                        total_cost + grid[x + dx, y + dy],
                        (x + dx, y + dy),
                        (last_bearings + [(dx, dy)]),
                    ),
                )
                # print(
                #     f"added via {dx, dy} from {x, y}",
                #     total_cost + grid[x + dx, y + dy],
                #     (x + dx, y + dy),
                #     (last_bearings + [(dx, dy)]),
                # )
            except KeyError:
                # off the grid
                pass
    raise ValueError("Never made it!")


@cache
def must_go_straight(path: tuple[tuple[int, int]]) -> bool:
    """Must we keep going straight?"""
    if len(path) < 4:
        return True
    last_seen = path[-1]
    time_in_direction = 1
    for step in reversed(path[:-1]):
        if step == last_seen:
            time_in_direction += 1
        else:
            break
    return time_in_direction < 4


def part2(puzzle: str) -> int:
    """Find the path with the lowest cost with the caveat that you can't go straight more than 10x"""
    start = (0, 0)
    grid = parse_input(puzzle)
    dest = max(grid)
    # print(dest)
    # so, our conditions that we need to track:
    # 1. total cost
    # 2. position
    # 3. last bearings
    last_bearings = []
    total_cost = 0
    paths = [
        (total_cost, start, last_bearings),
    ]
    heapq.heapify(paths)
    lowest_costs = {}
    while paths:
        total_cost, start, last_bearings = heapq.heappop(paths)
        print(total_cost, start, len(paths), " " * 10, end="\r")
        if start == dest:
            print("")
            if must_go_straight(tuple(last_bearings)):
                print("false positive after", total_cost)
                continue
            print("I made it!", total_cost)
            return total_cost
        been_here_lookup = (start, tuple(last_bearings[-10:]))
        try:
            # have we been here for cheaper?
            lowest_costs[been_here_lookup]
        except KeyError:
            lowest_costs[been_here_lookup] = total_cost
        else:
            # we already have
            continue
        valid_turns = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if last_bearings:
            last_x, last_y = last_bearings[-1]
            # print(f"{last_x=}, {last_y=}")
            # can't go backwards
            valid_turns.remove(
                (
                    -last_x if last_x else 0,
                    -last_y if last_y else 0,
                )
            )
            if must_go_straight(tuple((last_bearings))):
                # print("must go straight")
                # must go straiight at least 4x to start
                valid_turns = [last_bearings[-1]]
            elif len(last_bearings) >= 10 and set(last_bearings[-10:]) == {
                last_bearings[-1]
            }:
                # print("must turn")
                valid_turns.remove(last_bearings[-1])
        # print(valid_turns)
        x, y = start
        for dx, dy in valid_turns:
            try:
                heapq.heappush(
                    paths,
                    (
                        total_cost + grid[x + dx, y + dy],
                        (x + dx, y + dy),
                        (last_bearings + [(dx, dy)]),
                    ),
                )
                # print(
                #      f"added via {dx, dy} from {x, y}",
                #      total_cost + grid[x + dx, y + dy],
                #      (x + dx, y + dy),
                #      (last_bearings + [(dx, dy)]),
                #  )
            except KeyError:
                # off the grid
                pass
    raise ValueError("Never made it!")


def main():
    start = perf_counter()
    part_1_result = part1(TEST_INPUT)
    after_test_1 = perf_counter()
    assert part_1_result == 102, part_1_result
    before_1 = perf_counter()
    print(part1(REAL_INPUT))
    after_1 = perf_counter()
    part_2_result = part2(TEST_INPUT)
    after_test_2 = perf_counter()
    assert part_2_result == 94, part_2_result
    before_test_2a = perf_counter()
    part_2_other_test = part2(PART_2_TEST_INPUT)
    after_test_2a = perf_counter()
    assert part_2_other_test == 71, part_2_other_test
    before_2 = perf_counter()
    print(part2(REAL_INPUT))
    after_2 = perf_counter()
    print(f"part 1 test: {after_test_1 - start}")
    print(f"part 1 real: {after_1 - before_1}")
    print(f"part 2 tests: {after_test_2 - after_1}, {after_test_2a - before_test_2a}")
    print(f"part 2 real: {after_2 - before_2}")


if __name__ == "__main__":
    main()
