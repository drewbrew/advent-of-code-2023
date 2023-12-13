from pathlib import Path
from itertools import batched

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

REAL_INPUT = Path('day13.txt').read_text()


def find_horizontal_reflection(puzzle: list[str]) -> int:
    print(f'finding reflection for {puzzle}')
    for y, row in enumerate(puzzle):
        try:
            if puzzle[y + 1] == row:
                print('yay', y)
                # we have a reflection!
                return y + 1
                
        except IndexError:
            raise ValueError('end of the line?')

def find_reflection(horizontal_puzzle: str, vertical_puzzle: str) -> tuple[int, int]:
    """given the puzzle, find the reflection offsets
    """
    lines = horizontal_puzzle.splitlines()
    # start with the easy option: reflection along the x axis
    vertical_reflection_index = find_horizontal_reflection(lines)

    vertical_puzzle_lines = vertical_puzzle.splitlines()
    vertical_lines = []
    for x in range(len(vertical_puzzle_lines[0])):
        column = []
        for y in range(len(vertical_puzzle_lines)):
            column.append(vertical_puzzle_lines[y][x])
        vertical_lines.append(''.join(column))
    print(vertical_puzzle,'\n--\n', vertical_lines)
    horizontal_reflection_index = find_horizontal_reflection(vertical_lines)
    return horizontal_reflection_index, vertical_reflection_index

def part1(puzzle: str) -> int:
    puzzles = puzzle.split('\n\n')
    horizontal_score = 0
    vertical_score = 0
    for vertical, horizontal in batched(puzzles, n=2):
        h, v = find_reflection(horizontal, vertical)
        horizontal_score += h
        vertical_score += v
    return 100 * v + h


def main():
    part_1_score = part1(TEST_INPUT)
    assert part_1_score == 405, part_1_score
    print(part1(REAL_INPUT))

if __name__ == '__main__':
    main()