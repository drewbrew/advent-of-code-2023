"""Day 3: gear ratios"""

from pathlib import Path

TEST_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

REAL_INPUT = Path("day03.txt").read_text()

GridType = dict[tuple[int, int], str]


def parse_input(puzzle_input: str) -> GridType:
    grid = {}
    for y, line in enumerate(puzzle_input.splitlines()):
        for x, char in enumerate(line):
            if char == ".":
                continue
            grid[x, y] = char
    return grid


def adjacent_to_symbol(x: int, y: int, grid: GridType) -> bool:
    """Are any characters adjacent to me a non-digit?"""
    neighbors = [
        # up
        (x, y - 1),
        # down
        (x, y + 1),
        # left
        (x - 1, y),
        # up and left
        (x - 1, y - 1),
        # down and left
        (x - 1, y + 1),
    ]
    try:
        if grid[x, y].isdigit():
            # only look to the right if the active char is a digit
            neighbors.extend(
                [
                    # right
                    (x + 1, y),
                    # up and right
                    (x + 1, y - 1),
                    # down and right
                    (x + 1, y + 1),
                ]
            )
    except KeyError:
        pass
    for neighbor in neighbors:
        try:
            if not grid[neighbor].isdigit():
                return True
        except KeyError:
            pass
    return False


def part_numbers_on_row(y: int, max_x: int, grid: GridType) -> list[int]:
    """find all the numbers on the row which are adjacent to a non-digit"""
    running_total = 0
    result = []
    is_part_number = False
    for x in range(max_x + 1):
        try:
            val = int(grid[x, y])
        except (KeyError, ValueError):
            if running_total:
                # we've reached the end of a number:
                if not is_part_number:
                    if adjacent_to_symbol(x, y, grid=grid):
                        is_part_number = True
                if is_part_number:
                    result.append(running_total)
            running_total = 0
            is_part_number = False
        else:
            running_total = 10 * running_total + val
            if not is_part_number:
                if adjacent_to_symbol(x, y, grid=grid):
                    is_part_number = True
    return result


def part1(puzzle_input: str) -> int:
    grid = parse_input(puzzle_input)
    min_y = 0
    max_y = max(y for _, y in grid)
    max_x = max(x for x, _ in grid) + 1
    score = 0
    for row in range(min_y, max_y + 1):
        part_numbers = part_numbers_on_row(row, max_x, grid)
        # print(row, part_numbers)
        score += sum(part_numbers)
    return score


def find_number_adjacent_to_coordinate(x: int, y: int, grid: GridType) -> int:
    # start going left until we find a not-digit or gap
    min_x = 100000
    for x1 in range(x, -1, -1):
        if grid.get((x1, y), "").isdigit():
            min_x = x1
        else:
            break
    max_x = -1
    # my grid is 140 wide
    for x1 in range(x, 150):
        if grid.get((x1, y), "".isdigit()):
            max_x = x1
        else:
            break

    running_total = 0
    for x1 in range(min_x, max_x + 1):
        try:
            running_total = running_total * 10 + int(grid[x1, y])
        except ValueError:
            if grid[x1, y] == "*":
                break
            raise
    return running_total


def adjacent_numbers_to_coordinate(
    x: int, y: int, max_x: int, grid: GridType
) -> set[int]:
    """
    Find all numbers adjacent to the given coordinate.

    There _should_ be exactly two, but that's up to the caller to handle.
    """
    # start looking up
    y1 = y - 1
    found_numbers = set()
    for x1 in range(x - 1, x + 2):
        if grid.get((x1, y1), "").isdigit():
            adjacent_number = find_number_adjacent_to_coordinate(x1, y1, grid)
            if adjacent_number:
                found_numbers.add(adjacent_number)
    # now down
    y1 = y + 1
    for x1 in range(x - 1, x + 2):
        if grid.get((x1, y1), "").isdigit():
            adjacent_number = find_number_adjacent_to_coordinate(x1, y1, grid)
            if adjacent_number:
                found_numbers.add(adjacent_number)
    # now left
    if grid.get((x - 1, y), "").isdigit():
        if (x, y) == (58, 3):
            print("left:", grid[x - 1, y])
        adjacent_number = find_number_adjacent_to_coordinate(x - 1, y, grid)
        if adjacent_number:
            found_numbers.add(adjacent_number)
    # and right
    if grid.get((x + 1, y), "").isdigit():
        adjacent_number = find_number_adjacent_to_coordinate(x + 1, y, grid)
        if adjacent_number:
            found_numbers.add(adjacent_number)
    # if len(found_numbers) == 2:
    #     print(f"found gear at {x, y}: {found_numbers}")
    return found_numbers


def part2(puzzle_input: str) -> int:
    grid = parse_input(puzzle_input)
    max_x = max(x for x, _ in grid) + 1
    gears = [coordinate for coordinate, value in grid.items() if value == "*"]
    # print(gears)
    score = 0
    for gear in gears:
        x, y = gear
        adjacents = adjacent_numbers_to_coordinate(x, y, max_x, grid)
        try:
            adjacent_1, adjacent_2 = adjacents
        except ValueError:
            # not adjacent to 2
            # print(f"no gear at {x, y}: {adjacents}")
            continue
        score += adjacent_1 * adjacent_2
    return score


def main():
    test_result = part1(TEST_INPUT)
    assert test_result == 4361, test_result
    print(part1(REAL_INPUT))
    test_result = part2(TEST_INPUT)
    assert test_result == 467835, test_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
