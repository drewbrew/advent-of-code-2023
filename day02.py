"""day 2: cube conundrum"""

from pathlib import Path

REAL_INPUT = Path("day02.txt").read_text()

TEST_CONDITION = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

TEST_INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def part1(puzzle_input: str, conditions: dict[str, int]) -> int:
    total = 0
    for line in puzzle_input.splitlines():
        game_info, game_data = line.split(": ")
        game_number = int(game_info.split()[1])
        possible = True
        for draws in game_data.split("; "):
            for draw in draws.split(", "):
                number, color = draw.split()
                number = int(number)
                available = conditions[color]
                if available < number:
                    possible = False
                    break
            if not possible:
                break
        else:
            # print(game_number, possible)
            total += game_number
    return total


def part2(puzzle_input: str) -> int:
    """find the total power for the games"""
    total = 0
    for line in puzzle_input.splitlines():
        _, game_data = line.split(": ")
        power = 0
        score = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for draws in game_data.split("; "):
            for draw in draws.split(", "):
                number, color = draw.split()
                number = int(number)
                score[color] = max(score[color], number)
        power = score["blue"] * score["green"] * score["red"]
        total += power
    return total


def main():
    part_1_result = part1(TEST_INPUT, TEST_CONDITION)
    assert part_1_result == 8, part_1_result
    print(part1(REAL_INPUT, TEST_CONDITION))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 2286, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
