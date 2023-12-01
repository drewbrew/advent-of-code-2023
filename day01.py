import re
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


def part2_alt(puzzle_input: str) -> int:
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
    } | {str(i): i for i in range(1, 10)}
    regex = re.compile(rf'({"|".join(values)})')
    reversed_regex = re.compile(rf'({"|".join(i[::-1] for i in values)})')
    total = 0
    for line in puzzle_input.splitlines():
        first_digit = values[regex.search(line).group(0)]
        last_digit = values[reversed_regex.search(line[::-1]).group(0)[::-1]]
        score = first_digit * 10 + last_digit
        total += score
    return total


def part2(puzzle_input: str) -> int:
    lines = [line.strip() for line in puzzle_input.splitlines()]
    total = 0
    for line in lines:
        digits = digits_in_line(line)

        value = digits[0] * 10 + digits[-1]
        # print(line, value)
        total += value
    return total


def digits_in_line(line: str) -> list[int]:
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
    } | {str(i): i for i in range(1, 10)}
    first_chars = {char[0] for char in values}
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
                    break
    return digits


def main():
    test_value = 142
    assert part1(TEST_INPUT) == test_value, part1(TEST_INPUT)

    real_input = Path("day01.txt").read_text()
    print(part1(real_input))
    part_2_result = part2(PART_2_TEST_INPUT)
    assert part_2_result == 281, part_2_result
    part_2_alt_version = part2_alt(PART_2_TEST_INPUT)
    assert part_2_alt_version == 281, part_2_alt_version
    part_2_answer = part2(real_input)
    print(part_2_answer)
    alt_version = part2_alt(real_input)
    assert alt_version == part_2_answer, 'Regex version failed!'


if __name__ == "__main__":
    main()
