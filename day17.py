"""Day 17: don't go chasing lavafalls"""

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
    bearing = (1, 0)
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


def part2(puzzle: str) -> int:
    """Find the path with the lowest cost with the caveat that you can't go straight more than 10x"""
    start = (0, 0)
    grid = parse_input(puzzle)
    bearing = (1, 0)
    dest = max(grid)
    max_x, max_y = dest
    assert max_x == max_y  # making this a square
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
        print(total_cost, start, last_bearings)
        if start == dest:
            # print("I made it!", last_bearings, start)
            return total_cost
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
            # print(f'removed {(-last_x if last_x else 0, -last_y if last_y else 0)}')
        except IndexError:
            # first turn
            assert total_cost == 0
        if last_bearings and set(last_bearings[-10:]) == {last_bearings[-1]}:
            valid_turns.remove(last_bearings[-1])
        # print(valid_turns)
        try:
            # have we been here for cheaper?
            lowest_costs[(start, tuple(sorted(valid_turns)))]
        except KeyError:
            lowest_costs[(start, tuple(sorted(valid_turns)))] = total_cost
        else:
            # we already have
            continue
        x, y = start
        for dx, dy in valid_turns:
            if last_bearings[-10:] == [(dx, dy) for _ in range(10)]:
                print(f"skipping {dx, dy}")
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
    # part_1_result = part1(TEST_INPUT)
    # assert part_1_result == 102, part_1_result
    # print(part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 94, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
