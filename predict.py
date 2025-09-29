from collections import Counter
from card import Card
from deck import create_deck, shuffle_deck
from poker_hand import compare_hands, evaluate_hand


def simulate_win_rate(hand, community_cards, num_players, num_trials = 10000):
    win = lose = 0
    hand_type_counter = Counter()

    for _ in range(num_trials):
        deck = create_deck()
        used_cards = hand + community_cards
        deck = [c for c in deck if c not in used_cards]
        shuffle_deck(deck)

        opp_hands = []
        for _ in range(num_players - 1):
            opp_hand = [deck.pop() for _ in range(2)]
            opp_hands.append(opp_hand)

        tmp_community_cards = community_cards.copy()
        while len(tmp_community_cards) < 5:
            tmp_community_cards.append(deck.pop())

        tmp_hand = hand + tmp_community_cards
        all_hands = [tmp_hand]
        for opp_hand in opp_hands:
            all_hands.append(opp_hand + tmp_community_cards)
        #print(all_hands)
        winners, win_hand, _ = compare_hands(all_hands)
        if 0 in winners:
            win += 1
        else:
            lose += 1
        #print(f"winners: {winners}, win_hand: {win_hand}")
        hand_type, _ = evaluate_hand(tmp_hand)
        hand_type_counter[hand_type] += 1

    total = win + lose
    return win, lose, win/total




"""
exp_deck = create_deck()
shuffle_deck(exp_deck)
hand1 = []
hand2 = []
for i in range(2):
    hand1.append(exp_deck.pop())
    hand2.append(exp_deck.pop())
community_cards = []
for i in range(3):
    community_cards.append(exp_deck.pop())

win, lose, winrate = simulate_win_rate(hand1, community_cards, 3, 10000)
print(f"\nhand: {hand1}, community: {community_cards}")
print(f"win: {win}, lose: {lose}, winrate: {winrate}")
"""