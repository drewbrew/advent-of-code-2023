"""day 14: rolling rocks"""
from functools import cache
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


@cache
def move_north(puzzle: str) -> str:
    """
    Do a single iteration of moving everything northward that can move north
    """
    # old_grid = grid
    grid = parse_input(puzzle)
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
    return puzzle_to_string(grid)


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
    grid = move_north(puzzle)
    score = 0
    for weight, row in enumerate(reversed(parse_input(grid)), start=1):
        score += weight * sum(rolling is True for rolling in row)
    return score


def rotate_90(puzzle: str) -> str:
    return "\n".join(map("".join, zip(*(puzzle.split())[::-1])))


def part2(puzzle: str) -> int:
    seen: dict[str, int] = {}
    turns = 0
    original_puzzle = puzzle
    repeated = False
    while turns < 1_000_000_000:
        turns += 1
        for _ in range(4):
            puzzle = move_north(puzzle)
            puzzle = rotate_90(puzzle)
        if original_puzzle == TEST_INPUT:
            if turns == 1:
                stringified = puzzle
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
                stringified = puzzle
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
                stringified = puzzle
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
        if not repeated:
            try:
                old_turn = seen[puzzle]
            except KeyError:
                seen[puzzle] = turns
            else:
                print("repeat after turn", turns, "from", old_turn)
                repeated = True
                delta = turns - old_turn
                while turns <= 1_000_000_000:
                    turns += delta
                turns -= delta

    score = 0
    for weight, row in enumerate(reversed(parse_input(puzzle)), start=1):
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
