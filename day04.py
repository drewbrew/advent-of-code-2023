"""Day 4: scratch cards, or wtf kind of lottery are they running here?"""
from pathlib import Path
from collections import defaultdict

TEST_INPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


REAL_INPUT = Path("day04.txt").read_text()


def part1(puzzle_input: str) -> int:
    score = 0
    for line in puzzle_input.splitlines():
        card_info, card = line.split(": ")
        winners, card_data = card.split(" | ")
        winning_numbers = {int(i) for i in winners.split()}
        card_numbers = {int(i) for i in card_data.split()}
        matches = winning_numbers.intersection(card_numbers)
        if not matches:
            continue
        score += 2 ** (len(matches) - 1)
    return score


def part2(puzzle_input: str) -> int:
    cards = {}
    for line in puzzle_input.splitlines():
        card_info, card = line.split(": ")
        winners, card_data = card.split(" | ")
        game_number = int(card_info.split()[1])
        winning_numbers = {int(i) for i in winners.split()}
        card_numbers = {int(i) for i in card_data.split()}
        matches = winning_numbers.intersection(card_numbers)
        cards[game_number] = len(matches)
    # print(cards)
    # you start with one copy of each card
    copies_of_cards = defaultdict(lambda: 1)
    for card_number, matches in cards.items():
        copies = copies_of_cards[card_number]
        for earned_card in range(card_number + 1, card_number + matches + 1):
            if earned_card not in cards:
                continue
            # print(
            #     f"{card_number=}, {matches=}, {earned_card=},"
            #     f" {copies_of_cards[earned_card]}, {copies=}"
            # )
            copies_of_cards[earned_card] += copies

    # print(copies_of_cards)
    return sum(copies_of_cards.values())


def main():
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 13, part_1_result
    print(part1(REAL_INPUT))
    part_2_result = part2(TEST_INPUT)
    assert part_2_result == 30, part_2_result
    print(part2(REAL_INPUT))


if __name__ == "__main__":
    main()
