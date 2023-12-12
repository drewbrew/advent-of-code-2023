from pathlib import Path
from functools import cache

TEST_INPUT = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

REAL_INPUT = Path("day12.txt").read_text()


def parse_input(puzzle: str, part2: bool = False) -> list[tuple[str, tuple[int]]]:
    output = []
    for line in puzzle.splitlines():
        options, combos = line.split()
        if part2:
            combos = ",".join([combos, combos, combos, combos, combos])
            options = "?".join([options, options, options, options, options])

        numbers = tuple(int(i) for i in combos.split(","))
        output.append((options, numbers))
    return output


def valid_in_progress(survey: str, combinations: list[int]) -> bool:
    """Given a partially filled-in line, does it meet the survey conditions so far?"""
    found_results = []
    in_progress = False
    current_tally = 0
    for spot in survey:
        if spot == "?":
            raise ValueError("You forgot to sub out")
        if spot == "#":
            in_progress = True
            current_tally += 1
        elif in_progress:
            in_progress = False
            assert current_tally != 0, current_tally
            found_results.append(current_tally)
            current_tally = 0
    # don't save the last one this time because we might still be in progress!
    # print("---", survey, found_results, combinations)
    return found_results == list(combinations[: len(found_results)])


def line_meets_survey(survey: list[bool], combinations: tuple[int]) -> bool:
    """Given a filled-in line, does it meet the survey conditions?"""
    found_results = []
    in_progress = False
    current_tally = 0
    for spot in survey:
        if spot == "?":
            raise ValueError("You forgot to sub out")
        if spot == "#":
            in_progress = True
            current_tally += 1
        elif in_progress:
            in_progress = False
            assert current_tally != 0, current_tally
            found_results.append(current_tally)
            current_tally = 0
    if in_progress:
        found_results.append(current_tally)
    # print("---", survey, found_results, combinations)
    return found_results == list(combinations)


@cache
def fit_count(survey: str, counts: tuple[int]) -> int:
    # print(f"{survey=}, {counts=}")
    if not counts:
        return int("#" not in survey)

    # what's our biggest group?
    biggest = max(counts)
    biggest_index = counts.index(biggest)
    left_counts, right_counts = counts[:biggest_index], counts[biggest_index + 1 :]

    start_buffer = sum(left_counts) + len(left_counts)
    end_buffer = sum(right_counts) + len(right_counts)

    total = 0
    for index in range(start_buffer, len(survey) - end_buffer - biggest + 1):
        # split at the biggest and recursively check
        block_pattern = survey[index : index + biggest]
        left_border = "" if not index else survey[index - 1]
        right_border = "" if index + biggest == len(survey) else survey[index + biggest]
        # print(index, block_pattern, left_border, right_border)
        if "." not in block_pattern and left_border != "#" and right_border != "#":
            # if we have a valid large block that can be swapped around, find our boundary
            # counts and multipy them together
            left_total = fit_count(survey[: index - len(left_border)], left_counts)
            right_total = fit_count(
                survey[index + biggest + len(right_border) :], right_counts
            )
            total += left_total * right_total
    return total


def valid_combos(survey: str, combinations: tuple[int]) -> int:
    """How many valid combinations fit the survey pattern?"""
    attempts = [""]
    for item in survey:
        if item != "?":
            attempts = [i + item for i in attempts]
        else:
            attempts = [i + "#" for i in attempts] + [i + "." for i in attempts]
        if item == ".":
            # prune ones that are definitely invalid
            attempts = [
                attempt
                for attempt in attempts
                if valid_in_progress(attempt, combinations)
            ]
    # print(survey, combinations, len(attempts))
    # print(combinations, survey, "\n".join(str(i) for i in attempts))
    return sum(
        line_meets_survey(attempt, combinations=combinations) for attempt in attempts
    )


def part1(puzzle: str) -> int:
    lines = parse_input(puzzle=puzzle)
    score = 0
    for survey, combos in lines:
        s = valid_combos(survey, combos)
        # print(survey, combos, s)
        score += s
    return score


def part2(puzzle: str) -> int:
    lines = parse_input(puzzle=puzzle, part2=True)
    score = 0
    for survey, combos in lines:
        s = fit_count(survey, combos)
        # print(survey, combos, s)
        score += s
    return score


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 21, part_1_result
    print(part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 525152, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
