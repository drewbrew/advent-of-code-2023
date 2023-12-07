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


# ranks:
# 1. quints
# 2. quads
# 3. full house
# 4. trips
# 5. two pair
# 6. one pair
# 7. high card
CARD_RANKS = {
    char: value
    for value, char in enumerate(
        "23456789TJQKA",
        start=2,
    )
}
CARD_RANKS_P2 = {
    char: value
    for value, char in enumerate(
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
            (CARD_RANKS if not part_2 else CARD_RANKS_P2)[char] for char in self.hand
        )

    def __lt__(self, other: Self) -> bool:
        # print(self, other, "lt")
        if self.hand_rank < other.hand_rank:
            # print("hand rank wins")
            return True
        elif self.hand_rank == other.hand_rank and self.card_ranks < other.card_ranks:
            # print("card rank wins")
            return True
        # print("no")
        return False

    def __str__(self):
        return f"{self.hand} {self.bid} {self.hand_rank} {self.card_ranks}"

    def __repr__(self):
        return f"Hand('{self}')"


def hand_rank(hand: str) -> int:
    """Rank the hand from low to high for easy reversing"""
    c = Counter(hand)
    # print(hand, c, list(c.values()))
    if list(c.values()) == [5]:
        # print(hand, "quint")
        return 7
    if set(c.values()) == {4, 1}:
        # print(hand, "quad")
        return 6
    if set(c.values()) == {3, 2}:
        # print(hand, "full")
        # full house
        return 5
    if set(c.values()) == {3, 1}:
        # print(hand, "trips")
        # trips
        return 4
    if sorted(c.values(), reverse=True) == [2, 2, 1]:
        # two pair
        # print(hand, "2p")
        return 3
    if set(c.values()) == {2, 1}:
        # 1 pair
        # print(hand, "1p")
        return 2
    # high card
    # print(hand, "hc")
    return 1


def hand_rank_p2(hand: str) -> int:
    if "J" not in hand:
        return hand_rank(hand)
    return max(hand_rank(hand.replace("J", card)) for card in "AKQT98765432")


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
