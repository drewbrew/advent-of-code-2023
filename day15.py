"Day 15: hashing some lenses"

from pathlib import Path


TEST_INPUT = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

REAL_INPUT = Path("day15.txt").read_text().replace("\n", "")


def hash_character(char: str, starting_value: int = 0) -> int:
    return ((ord(char) + starting_value) * 17) % 256


def hash_string(string: str) -> int:
    score = 0
    for char in string:
        score = hash_character(char, score)
    return score


def part1(puzzle: str) -> int:
    return sum(hash_string(substr) for substr in puzzle.split(","))


def part2(puzzle: str) -> int:
    # NOTE: Thank $DEITY for preserving dictionary order insertion!
    boxes: list[dict[str, int]] = [{} for _ in range(256)]
    for instr in puzzle.split(","):
        if instr.endswith("-"):
            box_number = hash_string(instr[:-1])
            try:
                del boxes[box_number][instr[:-1]]
            except KeyError:
                pass
        else:
            assert instr[-2] == "="
            label, focal_length = instr.split("=")
            box_number = hash_string(label)
            boxes[box_number][label] = int(focal_length)
    total = 0
    for box_number, box in enumerate(boxes, start=1):
        box_power = sum(
            box_number * box_index * focal_length
            for box_index, focal_length in enumerate(box.values(), start=1)
        )
        total += box_power
    return total


def main():
    assert hash_string("HASH") == 52, hash_string("HASH")
    assert hash_string("rn") == 0, hash_string("rn")
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 1320, part_1_result
    print(part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 145, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
