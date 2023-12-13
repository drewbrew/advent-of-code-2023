"""day 13: point of incidence"""

from pathlib import Path

TEST_INPUT = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

REAL_INPUT = Path("day13.txt").read_text()


def is_valid_reflection_index(puzzle: list[str], upper_boundary: int) -> bool:
    """Is this an actual line of symmetry?

    work from the boundary up to the stop, stopping when we reach the end of
    the puzzle
    """
    valid = True
    # print("possible boundary at", upper_boundary)
    for offset in range(upper_boundary + 1):
        # print(offset, upper_boundary - offset, upper_boundary + offset + 1)
        try:
            upper_line = puzzle[upper_boundary - offset]
            lower_line = puzzle[upper_boundary + offset + 1]
        except IndexError:
            return valid
        # print(offset, upper_line, lower_line)
        if upper_line != lower_line:
            # print("no")
            return False
    return valid


def find_horizontal_reflection(
    puzzle: list[str],
    old_reflection: int | None = None,
) -> int:
    """Find the reflection along the X axis

    if old_reflection is set, exclude that row
    """
    # printable = "\n".join(puzzle)
    # print(f"finding reflection for\n{printable}")
    for y, row in enumerate(puzzle):
        # let this one raise out
        next_line = puzzle[y + 1]
        if y + 1 == old_reflection:
            continue

        if next_line == row and is_valid_reflection_index(puzzle, y):
            # print("yay", y)
            # we have a reflection!
            return y + 1
    raise ValueError("None found")


def find_reflection(
    puzzle: str,
    old_reflection: tuple[int, int] | None = None,
) -> tuple[int, int]:
    """given the puzzle, find the reflection offsets"""
    lines = puzzle.splitlines()
    # start with the easy option: reflection along the x axis
    try:
        vertical_reflection_index = find_horizontal_reflection(
            lines,
            old_reflection[1] if old_reflection else None,
        )
    except (IndexError, ValueError):
        pass
    else:
        # print("found reflection along X axis", vertical_reflection_index)
        return 0, vertical_reflection_index

    vertical_lines = []
    for x in range(len(lines[0])):
        column = []
        for y in range(len(lines)):
            column.append(lines[y][x])
        vertical_lines.append("".join(column))
    # print("\n--\n", "\n".join(vertical_lines))
    horizontal_reflection_index = find_horizontal_reflection(
        vertical_lines,
        old_reflection[0] if old_reflection else None,
    )
    # print("found along Y axis", horizontal_reflection_index)
    return horizontal_reflection_index, 0


def find_smudge(
    puzzle: str,
    old_reflection: tuple[int, int],
) -> tuple[int, int]:
    """Given the puzzle and the old reflection, find a bit flip that causes a new reflection"""
    lines = puzzle.splitlines()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            new_char = "." if char == "#" else "."
            new_lines = (
                lines[:y]
                + ["".join(line[:x]) + new_char + "".join(line[x + 1 :])]
                + lines[y + 1 :]
            )
            try:
                new_reflection = find_reflection(
                    "\n".join(new_lines),
                    old_reflection=old_reflection,
                )
            except IndexError:
                continue
            if new_reflection != old_reflection:
                return new_reflection
    raise ValueError(f"Could not find a smudge for {puzzle}")


def run_puzzle(puzzle: str) -> tuple[int, int]:
    puzzles = puzzle.split("\n\n")
    horizontal_score = 0
    vertical_score = 0

    p2_horizontal_score = 0
    p2_vertical_score = 0
    for puzzle in puzzles:
        h, v = find_reflection(puzzle)
        horizontal_score += h
        vertical_score += v
        h2, v2 = find_smudge(puzzle, (h, v))
        # print(h, v, horizontal_score, vertical_score, h2, v2)
        p2_horizontal_score += h2
        p2_vertical_score += v2

    part_1_result = 100 * vertical_score + horizontal_score
    part_2_result = 100 * p2_vertical_score + p2_horizontal_score
    return part_1_result, part_2_result


def main():
    test_score = run_puzzle(TEST_INPUT)
    assert test_score == (405, 400), test_score
    print("\n".join(str(i) for i in run_puzzle(REAL_INPUT)))


if __name__ == "__main__":
    main()
