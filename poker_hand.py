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

    # check straight flush
    if straight_flush:
        if straight_flush[0] == 14:
            return ("Royal Flush", straight_flush)
        else:
            return ("Straight Flush", straight_flush)

    # check four of a kind
    if 4 in value_counter.values():
        quads = [v for v, c in value_counter.items() if c == 4][0]
        kicker = max([v for v in values if v != quads])
        return ("Four of a Kind", [quads, kicker])

    # check full house
    if 3 in value_counter.values() and 2 in value_counter.values():
        trips = max([v for v, c in value_counter.items() if c == 3])
        pair = max([v for v, c in value_counter.items() if c == 2])
        return ("Full House", [trips, pair])

    # check flush
    if flush_suit:
        top_flush = sorted([c.value for c in flush_cards], reverse=True)[:5]
        return ("Flush", top_flush)

    # check straight
    if straight:
        return ("Straight", straight)

    # check three of a kind
    if 3 in value_counter.values():
        trips = [v for v, c in value_counter.items() if c == 3][0]
        kickers = sorted([v for v in values if v != trips], reverse=True)[:2]
        return ("Three of a Kind", [trips] + kickers)

    # check pairs
    pairs = [v for v, c in value_counter.items() if c == 2]
    if len(pairs) >= 2:
        top_two = sorted(pairs, reverse=True)[:2]
        kicker = max(v for v in values if v not in top_two)
        return ("Two Pair", top_two + [kicker])

    if len(pairs) == 1:
        pair = pairs[0]
        kickers = sorted([v for v in values if v != pair], reverse=True)[:3]
        return ("One Pair", [pair] + kickers)

    # high card
    top_cards = sorted(values, reverse=True)[:5]
    return ("High Card", top_cards)

def get_straight(vals):
    vals = sorted(set(vals), reverse=True)
    for i in range(len(vals)-4):
        ret = vals[i:i+5]
        if ret[0] - ret[4] == 4:
            return ret
    return None

def compare_hands(hands:list[list[Card]]):
    """
    compare hands of all players
    return list of winners, highest hand, list of highest points
    """
    highest_player = []
    highest_rank = None
    highest_points = None
    for i in range(len(hands)):
        hand = hands[i]
        rank, points = evaluate_hand(hand)
        #debug
        #print(f"DEBUG: i: {i}, rank: {rank}, points: {points}")
        #!debug
        if not highest_rank:
            highest_rank = rank
            highest_points = points
            highest_player = [i]
            continue
        if HAND_RANKS[rank] > HAND_RANKS[highest_rank]:
            highest_rank = rank
            highest_points = points
            highest_player = [i]
        elif HAND_RANKS[rank] == HAND_RANKS[highest_rank]:
            if points > highest_points:
                highest_player = [i]
                highest_points = points
            elif points == highest_points:
                # same hand
                highest_player.append(i)
        else:
            continue
    return highest_player, highest_rank, highest_points