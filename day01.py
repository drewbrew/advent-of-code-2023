from pathlib import Path

TEST_INPUT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

PART_2_TEST_INPUT = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def part1(puzzle_input: str) -> int:
    lines = [line.strip() for line in puzzle_input.splitlines()]
    total = 0
    for line in lines:
        digits = [int(char) for char in line if char.isdigit()]
        value = digits[0] * 10 + digits[-1]
        # print(line, value)
        total += value
    return total


def part2(puzzle_input: str) -> int:
    lines = [line.strip() for line in puzzle_input.splitlines()]
    total = 0
    values = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "zero": 0,
    } | {str(i): i for i in range(10)}
    first_chars = {char[0] for char in values}
    for line in lines:
        digits = []
        for index, char in enumerate(line):
            if char in first_chars:
                # print(char, line[index : index + 5])
                if char.isdigit():
                    digits.append(int(char))
                    continue
                for offset in range(3, 6):
                    try:
                        value = values[line[index : index + offset]]
                    except KeyError:
                        pass
                    else:
                        digits.append(value)
                        continue

        value = digits[0] * 10 + digits[-1]
        # print(line, value)
        total += value
    return total


def main():
    test_value = 142
    assert part1(TEST_INPUT) == test_value, part1(TEST_INPUT)

    real_input = Path("day01.txt").read_text()
    print(part1(real_input))
    part_2_result = part2(PART_2_TEST_INPUT)
    assert part_2_result == 281, part_2_result
    print(part2(real_input))


if __name__ == "__main__":
    main()
