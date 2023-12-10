import pathlib
from datetime import datetime
from collections import Counter
from utils import get_input, read_input

input_file = "input.txt"

if not pathlib.Path(input_file).exists():
    str_input = get_input(year=2023, day=datetime.now().day)

files = ["example.txt", input_file]


def classify_hand_with_joker(hand, hand_strength, joker=False):
    """
    Classify a poker hand.
    """
    best_hand_type = classify_hand(hand)
    if joker and "J" in hand:
        for c in "AKQT98765432":
            new_hand = hand.replace("J", c)
            new_hand_type = classify_hand(new_hand)
            if hand_strength[new_hand_type] > hand_strength[best_hand_type]:
                best_hand_type = new_hand_type
    return best_hand_type


def classify_hand(hand):
    counts = Counter(hand)
    freqs = list(counts.values())
    if 5 in freqs:
        return "Five of a Kind"
    if 4 in freqs:
        return "Four of a Kind"
    if freqs.count(3) == 1 and freqs.count(2) == 1:
        return "Full House"
    if 3 in freqs:
        return "Three of a Kind"
    if freqs.count(2) == 2:
        return "Two Pair"
    if 2 in freqs:
        return "One Pair"
    return "High Card"


def replace_hand_labels(hand, joker=False):
    old_to_new = {
        "2": "A",
        "3": "B",
        "4": "C",
        "5": "D",
        "6": "E",
        "7": "F",
        "8": "G",
        "9": "H",
        "T": "I",
        "J": "1" if joker else "J",
        "Q": "K",
        "K": "L",
        "A": "M"
    }
    new_labels = ""
    for c in hand:
        new_labels += old_to_new[c]
    return new_labels


def sort_hands(hands, joker=False):
    hand_strength = {
        "High Card": 1,
        "One Pair": 2,
        "Two Pair": 3,
        "Three of a Kind": 4,
        "Full House": 5,
        "Four of a Kind": 6,
        "Five of a Kind": 7
    }

    # Classify the hands
    classified_hands = [(hand[:5], classify_hand_with_joker(hand[:5], hand_strength, joker), hand) for hand in hands]
    # Sort hands by type
    sorted_by_type = sorted(classified_hands, key=lambda x: hand_strength[x[1]])

    # Now, for hands of the same type, sort them by comparing cards
    sorted_hands = []
    sorted_hand_strength = sorted(hand_strength.keys(), key=lambda x: hand_strength[x])
    for hand_type in sorted_hand_strength:
        # Get all hands of the same type and replace the card labels with a new ranking for sorting
        same_type_hands = [(replace_hand_labels(hand[0], joker),) + hand for hand in sorted_by_type if hand[1] == hand_type]
        same_type_hands_sorted = sorted(same_type_hands, key=lambda x: x[0])
        sorted_hands.extend(same_type_hands_sorted)

    return [hand[3] for hand in sorted_hands]


def get_bid_rank_result(sorted_hands):
    r = 0
    for i, h in enumerate(sorted_hands):
        bid = int(h.split(sep=" ")[1].strip())
        bid_rank = bid * (i + 1)
        r += bid_rank
    return r


for f in files:
    list_input = read_input(f)
    # print(list_input)
    sorted_hands_p1 = sort_hands(list_input)
    print(f"{f} - Part 1: {get_bid_rank_result(sorted_hands_p1)}")
    sorted_hands_p2 = sort_hands(list_input, joker=True)
    print(f"{f} - Part 2: {get_bid_rank_result(sorted_hands_p2)}")
