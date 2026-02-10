from collections import Counter
from card import Card
from deck import create_deck, shuffle_deck
from poker_hand import compare_hands, evaluate_hand


def simulate_win_rate(hand, community_cards, num_players, num_trials=1000):
    win = lose = 0
    hand_type_counter = Counter()

    used_set = set((c.suit, c.value) for c in hand + community_cards)
    base_deck = [c for c in create_deck() if (c.suit, c.value) not in used_set]

    for _ in range(num_trials):
        deck = base_deck.copy()
        shuffle_deck(deck)

        opp_hands = []
        for _ in range(num_players - 1):
            opp_hands.append([deck.pop(), deck.pop()])

        sim_community = community_cards.copy()
        while len(sim_community) < 5:
            sim_community.append(deck.pop())

        all_hands = [hand + sim_community]
        for opp_hand in opp_hands:
            all_hands.append(opp_hand + sim_community)

        winners, win_hand, _ = compare_hands(all_hands)
        if 0 in winners:
            win += 1
        else:
            lose += 1

        hand_type, _ = evaluate_hand(all_hands[0])
        hand_type_counter[hand_type] += 1

    total = win + lose
    return win, lose, win / total
