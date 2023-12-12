from pathlib import Path

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
    print(survey, combinations, len(attempts))
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
        s = valid_combos(survey, combos)
        # print(survey, combos, s)
        score += s
    return score


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 21, part_1_result
    print("p1", part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 525152, part_2_result
    print("here goes")
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
