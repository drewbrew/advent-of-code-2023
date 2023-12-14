"""day 14: rolling rocks"""
from copy import deepcopy
from pathlib import Path

# NOTE: Chrome tried to ruin my input by "translating" from Portuguese


TEST_INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

REAL_INPUT = Path("day14.txt").read_text()


def parse_input(puzzle: str) -> list[list[bool | None]]:
    grid = []
    for line in puzzle.splitlines():
        grid.append(
            [
                {
                    "#": False,
                    "O": True,
                    ".": None,
                }[char]
                for char in line
            ]
        )
    return grid


def move_north(grid: list[list[bool | None]]):
    """
    Do a single iteration of moving everything northward that can move north
    """
    # old_grid = grid
    grid = deepcopy(grid)
    for y, row in enumerate(grid[1:], start=1):
        for x, rolling in enumerate(row):
            if rolling and grid[y - 1][x] is None:
                delta = 1
                try:
                    while grid[y - delta][x] is None:
                        delta += 1
                        if y - delta < 0:
                            break
                except IndexError:
                    # end of the board, don't care
                    pass
                delta -= 1
                # print(f"swapping from {y, x} to {y - delta, x}")
                grid[y - delta][x] = rolling
                row[x] = None
    # print_grid(old_grid)
    # print("---")
    # print_grid(grid)
    # print("====")
    return grid


def move_south(grid: list[list[bool | None]]) -> list[list[bool | None]]:
    """
    Do a single iteration of moving everything southward that can move south
    """
    # it's easiest to flip the grid vertically and flip back
    return list(reversed(move_north(list(reversed(grid)))))


def move_east(grid: list[list[bool | None]]) -> list[list[bool | None]]:
    grid = deepcopy(grid)
    for y, row in enumerate(grid):
        row_interim = list(reversed(row))
        # print(
        #     puzzle_to_string([row]),
        #     "became",
        #     puzzle_to_string([row_interim]),
        # )
        # this one is obnoxious: we have to work backwards
        for x, rolling in enumerate(row_interim[1:], start=1):
            if rolling and row_interim[x - 1] is None:
                delta = 1
                try:
                    while row_interim[x - delta] is None:
                        delta += 1
                        if x - delta < 0:
                            break
                except IndexError:
                    pass
                delta -= 1
                row_interim[x - delta] = rolling
                row_interim[x] = None
                # print("after swap at ", x, puzzle_to_string([row_interim]))
        # now save the fixed row

        grid[y] = list(reversed(row_interim))
        # print("and finally", puzzle_to_string([grid[y]]))
    return grid


def move_west(grid: list[list[bool | None]]) -> list[list[bool | None]]:
    grid = deepcopy(grid)
    for row in grid:
        for x, rolling in enumerate(row[1:], start=1):
            if rolling and row[x - 1] is None:
                delta = 1
                try:
                    while row[x - delta] is None:
                        delta += 1
                        if x - delta < 0:
                            break
                except IndexError:
                    pass
                delta -= 1
                row[x - delta] = rolling
                row[x] = None
    return grid


def puzzle_to_string(grid: list[list[bool | None]]) -> str:
    return "\n".join(
        "".join(
            {
                None: ".",
                True: "O",
                False: "#",
            }[rolling]
            for rolling in row
        )
        for row in grid
    )


def print_grid(grid: list[list[bool | None]]):
    for row in grid:
        for rolling in row:
            print(
                {
                    None: ".",
                    True: "O",
                    False: "#",
                }[rolling],
                end="",
            )
        print("")


def part1(puzzle: str) -> int:
    grid = parse_input(puzzle)

    new_grid = move_north(grid)
    score = 0
    for weight, row in enumerate(reversed(new_grid), start=1):
        score += weight * sum(rolling is True for rolling in row)
    return score


def part2(puzzle: str) -> int:
    grid = parse_input(puzzle)
    seen: dict[str, int] = {}
    turns = 0
    repeated = False
    while turns < 1_000_000_000:
        turns += 1
        grid = move_north(grid)
        # print("done with N")
        # print_grid(grid)
        grid = move_west(grid)
        # print("done with W")
        # print_grid(grid)
        grid = move_south(grid)
        # print("done with S")
        # print_grid(grid)
        grid = move_east(grid)
        # print("done with E")
        # print_grid(grid)

        if puzzle == TEST_INPUT:
            if turns == 1:
                stringified = puzzle_to_string(grid)
                assert (
                    stringified
                    == """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""
                ), stringified
                print("turn 1 ok")
            if turns == 2:
                stringified = puzzle_to_string(grid)
                assert (
                    stringified
                    == """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""
                ), stringified
                print("turn 2 ok")
            if turns == 3:
                stringified = puzzle_to_string(grid)
                assert (
                    stringified
                    == """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""
                ), stringified
                print("turn 3 ok")
        new_grid = puzzle_to_string(grid)
        if not repeated:
            try:
                old_turn = seen[new_grid]
            except KeyError:
                seen[new_grid] = turns
            else:
                print("repeat after turn", turns, "from", old_turn)
                repeated = True
                delta = turns - old_turn
                while turns <= 1_000_000_000:
                    turns += delta
                turns -= delta

    score = 0
    for weight, row in enumerate(reversed(grid), start=1):
        score += weight * sum(rolling is True for rolling in row)
    return score


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 136, part_1_result
    print(part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 64, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
