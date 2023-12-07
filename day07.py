"""Day 7: poker face"""

from collections import Counter
from pathlib import Path
from typing import Self

TEST_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

REAL_INPUT = Path("day07.txt").read_text()


CARD_RANKS = {
    card: value
    for value, card in enumerate(
        "23456789TJQKA",
        start=2,
    )
}
# for part 2, to balance jokers being wild, jokers count as low card
CARD_RANKS_P2 = {
    card: value
    for value, card in enumerate(
        "J23456789TQKA",
        start=1,
    )
}


class Hand:
    def __init__(self, line: str, part_2: bool = False):
        self.hand, bid = line.split()
        self.bid = int(bid)
        self.hand_rank = hand_rank(self.hand) if not part_2 else hand_rank_p2(self.hand)
        self.card_ranks = tuple(
            (CARD_RANKS if not part_2 else CARD_RANKS_P2)[card] for card in self.hand
        )

    def __lt__(self, other: Self) -> bool:
        # do the minimum for sorting, implementing __lt__
        # print(self, other, "lt")
        if self.hand_rank < other.hand_rank:
            # print("hand rank wins")
            return True
        return self.hand_rank == other.hand_rank and self.card_ranks < other.card_ranks

    def __str__(self):
        return f"{self.hand} {self.bid} {self.hand_rank} {self.card_ranks}"

    def __repr__(self):
        return f"Hand('{self}')"


def hand_rank(hand: str) -> int:
    """Rank the hand based on the rules of the game"""
    c = Counter(hand)
    # print(hand, c, list(c.values()))
    value_list = sorted(c.values(), reverse=True)
    match value_list:
        # ranks:
        # 1. quints
        # 2. quads
        # 3. full house
        # 4. trips
        # 5. two pair
        # 6. one pair
        # 7. high card
        case [5]:
            # five of a kind
            return 7
        case [4, 1]:
            # quads
            return 6
        case [3, 2]:
            # full house
            return 5
        case [3, 1, 1]:
            # trips
            return 4
        case [2, 2, 1]:
            # two pair
            return 3
        case [2, 1, 1, 1]:
            # one pair
            return 2
        case _:
            # high card
            return 1


def hand_rank_p2(hand: str) -> int:
    """Part 2: find the rank of the hand with jokers wild"""
    if "J" not in hand:
        return hand_rank(hand)
    replacements = "AKQT98765432"
    return max(hand_rank(hand.replace("J", card)) for card in replacements)


def part1(puzzle_input: str, part_2: bool = False) -> int:
    hands = [Hand(line, part_2=part_2) for line in puzzle_input.splitlines()]
    # print(list(sorted(hands)), "huh?")
    score = 0

    score = sum(
        hand.bid * index
        for index, hand in enumerate(
            sorted(hands),
            start=1,
        )
    )
    return score


def main():
    assert Hand("KTJJT 220") < Hand("KK677 28"), (
        Hand("KTJJT 220").card_ranks,
        Hand("KK677 28").card_ranks,
    )
    assert Hand("KK677 28") > Hand("KTJJT 220"), (
        Hand("KK677 28").card_ranks,
        Hand("KK677 28").hand_rank,
        Hand("KTJJT 220").card_ranks,
        Hand("KTJJT 220").hand_rank,
    )
    part_1_result = part1(TEST_INPUT)
    assert part_1_result == 6440, part_1_result
    print(part1(REAL_INPUT))
    part_2_result = part1(TEST_INPUT, True)
    assert part_2_result == 5905, part_2_result
    print(part1(REAL_INPUT, True))


if __name__ == "__main__":
    main()
