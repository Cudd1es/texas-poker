from collections import Counter

from card import Card

HAND_RANKS = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10,
}


def evaluate_hand(cards: list[Card]) -> (str, list[int]):
    """
    input: a list of cards to check
    output: a tuple with the hand name and list of card ranks
    """
    values = [c.value for c in cards]
    suits = [c.suit for c in cards]
    value_counter = Counter(values)
    suit_counter = Counter(suits)

    # check if flush exists
    flush_suit = None
    for suit, count in suit_counter.items():
        if count >= 5:
            flush_suit = suit
            break
    flush_cards = [c for c in cards if c.suit == flush_suit] if flush_suit else []

    # check if straight flush exists
    straight_flush = None
    if flush_suit:
        straight_flush = get_straight([c.value for c in flush_cards])

    # check if straight exists
    straight = None
    straight = get_straight(values)


def get_straight(vals):
    vals = sorted(set(vals), reverse=True)
    for i in range(len(vals)-4):
        ret = vals[i:i+5]
        if ret[0] - ret[4] == 4:
            return ret
    return None