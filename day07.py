import sys
from collections import defaultdict
from enum import Enum
from functools import total_ordering

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day07_test_input{suffix}.txt"
else:
    input_file = f"day07_input.txt"

data = utils.input_as_lines(input_file)


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_KIND = 6
    FIVE_OF_KIND = 7


CARD_SCORES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


@total_ordering
class Hand:
    def __init__(self, card_str, bid_str):
        self.cards = list(card_str)
        self.bid = int(bid_str)
        self.hand_type = None

        card_counts = defaultdict(lambda: 0)
        for c in self.cards:
            card_counts[c] += 1

        count_list = sorted(card_counts.values(), reverse=True)
        if count_list == [5]:
            self.hand_type = HandType.FIVE_OF_KIND
        elif count_list == [4, 1]:
            self.hand_type = HandType.FOUR_OF_KIND
        elif count_list == [3, 2]:
            self.hand_type = HandType.FULL_HOUSE
        elif count_list == [3, 1, 1]:
            self.hand_type = HandType.THREE_OF_KIND
        elif count_list == [2, 2, 1]:
            self.hand_type = HandType.TWO_PAIRS
        elif count_list == [2, 1, 1, 1]:
            self.hand_type = HandType.ONE_PAIR
        else:
            self.hand_type = HandType.HIGH_CARD

    def __lt__(self, other):
        if self.hand_type == other.hand_type:
            # Same hand, so compare cards in order
            for i, c1 in enumerate(self.cards):
                c2 = other.cards[i]
                if CARD_SCORES[c1] != CARD_SCORES[c2]:
                    return CARD_SCORES[c1] < CARD_SCORES[c2]
            return False
        else:
            return self.hand_type.value < other.hand_type.value

    def __eq__(self, other):
        return self.cards == other.cards

    def __str__(self):
        return "".join(self.cards)


hands = []

for line in data:
    cards, bid = line.split(" ")
    hands.append(Hand(cards, bid))

hands.sort()
p1_total = 0
for i, h in enumerate(hands):
    p1_total += (i + 1) * h.bid

print(f"Part 1: {p1_total}")

# Part 2

CARD_SCORES_2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


@total_ordering
class Hand2:
    def __init__(self, card_str, bid_str):
        self.cards = list(card_str)
        self.bid = int(bid_str)
        self.hand_type = None

        card_counts = defaultdict(lambda: 0)
        for c in self.cards:
            card_counts[c] += 1

        count_list = sorted(
            [v for k, v in card_counts.items() if k != "J"], reverse=True
        )
        if card_counts["J"] == 5 or count_list[0] + card_counts["J"] == 5:
            self.hand_type = HandType.FIVE_OF_KIND
        elif count_list[0] + card_counts["J"] == 4:
            self.hand_type = HandType.FOUR_OF_KIND
        elif (
            count_list[0] + card_counts["J"] >= 3
            and count_list[1] + card_counts["J"] - (3 - count_list[0]) >= 2
        ):
            self.hand_type = HandType.FULL_HOUSE
        elif count_list[0] + card_counts["J"] == 3:
            self.hand_type = HandType.THREE_OF_KIND
        elif (
            count_list[0] + card_counts["J"] >= 2
            and count_list[1] + card_counts["J"] - (2 - count_list[0]) >= 2
        ):
            self.hand_type = HandType.TWO_PAIRS
        elif count_list[0] + card_counts["J"] >= 2:
            self.hand_type = HandType.ONE_PAIR
        else:
            self.hand_type = HandType.HIGH_CARD

    def __lt__(self, other):
        if self.hand_type == other.hand_type:
            # Same hand, so compare cards in order
            for i, c1 in enumerate(self.cards):
                c2 = other.cards[i]
                if CARD_SCORES_2[c1] != CARD_SCORES_2[c2]:
                    return CARD_SCORES_2[c1] < CARD_SCORES_2[c2]
            return False
        else:
            return self.hand_type.value < other.hand_type.value

    def __eq__(self, other):
        return self.cards == other.cards

    def __str__(self):
        return "".join(self.cards)


hands = []

for line in data:
    cards, bid = line.split(" ")
    hands.append(Hand2(cards, bid))

hands.sort()
p1_total = 0
for i, h in enumerate(hands):
    p1_total += (i + 1) * h.bid

print(f"Part 2: {p1_total}")
