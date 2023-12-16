"""Day 16: the floor will be lava"""

from pathlib import Path

TEST_INPUT = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

REAL_INPUT = Path("day16.txt").read_text()


def display_path_hit(puzzle: str, spots_seen: set[tuple[complex, complex]]):
    positions = set(pos for pos, _ in spots_seen)
    for y, row in enumerate(puzzle.splitlines()):
        for x, char in enumerate(row):
            if x - (1j * y) in positions:
                print("#", end="")
            else:
                print(char, end="")
        print()


def part1(
    puzzle: str,
    start_position: complex = -1 + 0j,
    start_heading: complex = 1 + 0j,
) -> int:
    grid: dict[complex, str] = {}
    lines = puzzle.splitlines()
    assert len(set(len(line) for line in lines)) == 1
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            grid[x - (1j * y)] = char
    # position, bearing
    beams: set[tuple[complex, complex]] = {(start_position, start_heading)}
    spots_seen: set[tuple[complex, complex]] = set(list(beams))
    while beams:
        if puzzle == TEST_INPUT and len(beams) > 15:
            raise ValueError("uh no")
        old_spots_seen = sorted(
            (pos.real, pos.imag, heading.real, heading.imag)
            for pos, heading in spots_seen
        )
        new_beams = set()
        for position, bearing in beams:
            new_position = position + bearing
            # print(position, bearing, new_position, grid.get(new_position), len(beams))
            if (new_position, bearing) in spots_seen:
                continue
            spots_seen.add((new_position, bearing))
            try:
                match grid[new_position]:
                    case ".":
                        # simple case: save and continue
                        new_beams.add((new_position, bearing))
                    case "-":
                        if bearing in (1 + 0j, -1 + 0j):
                            # hits the pointy end, nothing happens
                            new_beams.add((new_position, bearing))
                        else:
                            # hits the flat end, two beams perpendicular happen

                            new_beams |= {
                                (new_position, 1 + 0j),
                                (new_position, -1 + 0j),
                            }
                    case "|":
                        if bearing in (1j, -1j):
                            # hits the pointy end, nothing happens
                            new_beams.add((new_position, bearing))
                        else:
                            # hits the flat end, two beams perpendicular happen
                            new_beams |= {
                                (new_position, 1j),
                                (new_position, -1j),
                            }
                    case "/":
                        # hits a reflection!
                        match bearing:
                            case 1 + 0j:
                                # going up
                                # print('hit /, going right to up')
                                bearing = 1j
                            case -1 + 0j:
                                # print('hit /, going left to down')
                                # going down
                                bearing = -1j
                            case 1j:
                                # going right
                                # print('hit /, going up to right')
                                bearing = 1 + 0j
                            case -1j:
                                # going left
                                # print('hit /, going down to left')
                                bearing = -1 + 0j
                            case _:
                                raise ValueError(f"Unknown direction {bearing}")
                        new_beams.add((new_position, bearing))
                    case "\\":
                        # other reflection!
                        match bearing:
                            case 1 + 0j:
                                # going down
                                # print('hit \\, going from right to down')
                                bearing = -1j
                            case -1 + 0j:
                                # going up
                                # print('hit \\, going from left to up')
                                bearing = 1j
                            case 1j:
                                # going left
                                # print('hit \\, going from up to left')
                                bearing = -1 + 0j
                            case -1j:
                                # going right
                                # print('hit \\, going from down to right')
                                bearing = 1 + 0j
                            case _:
                                raise ValueError(f"Unknown direction {bearing}")
                        new_beams.add((new_position, bearing))
                    case _:
                        raise ValueError(f"Unknown char {char}")
            except KeyError:
                # print('end of the world')
                spots_seen.remove((new_position, bearing))
        if (
            sorted(
                (pos.real, pos.imag, heading.real, heading.imag)
                for pos, heading in spots_seen
            )
            == old_spots_seen
        ):
            # print('done?')
            len(set(pos for pos, _ in spots_seen)) - 1
        beams = new_beams
        # display_path_hit(puzzle, spots_seen)
    # print('all beams finished')
    # display_path_hit(puzzle, spots_seen)
    return len(set(pos for pos, _ in spots_seen)) - 1


def part2(puzzle: str) -> int:
    """Find the starting position that gives the highest number of lit tiles"""
    # NOTE: mine found the right answer at x = 23, so I entered each one as it
    # came through as guesses because I didn't want to wait around for
    # the whole thing to finish
    min_x = 0
    max_y = 0
    lines = puzzle.splitlines()
    max_x = len(lines[0])
    min_y = 0 - len(lines)
    # start at the top, pointing down
    print("grid size", max_x, min_y)
    score = 0
    for x in range(min_x, max_x):
        score = max(
            part1(
                puzzle=puzzle,
                start_position=(x + 1j),
                start_heading=-1j,
            ),
            score,
        )
        # now from the bottom, going up
        score = max(
            part1(
                puzzle=puzzle,
                start_position=(x + min_y * 1j),
                start_heading=1j,
            ),
            score,
        )
        print(x, score)
    print("x result", score)
    for y in range(min_y + 1, max_y + 1):
        # from the left, going right
        start_heading = 1 + 0j
        score = max(
            part1(
                puzzle=puzzle,
                start_position=(-1 + 1j * y),
                start_heading=start_heading,
            ),
            score,
        )
        # from the right, going left
        start_heading = -1 + 0j
        score = max(
            part1(
                puzzle=puzzle,
                start_position=(max_x + 1j * y),
                start_heading=start_heading,
            ),
            score,
        )
        print(y, score)
    return score


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 46, part_1_result
    print(part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 51, part_2_result
    print("part 2: go")
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
