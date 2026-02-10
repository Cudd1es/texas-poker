from card import Card
from deck import create_deck, shuffle_deck, deal_hands, card_sort_key, sort_hand


def test_create_deck():
    deck = create_deck()
    assert len(deck) == 52


def test_deal_hands():
    deck = create_deck()
    hands, remaining = deal_hands(deck, num_players=3)
    assert len(hands) == 3
    assert all(len(h) == 2 for h in hands)
    assert len(remaining) == 46


def test_card_sort_key():
    c = Card('h', 10)
    key = card_sort_key(c)
    assert key == (10, 1)  # h is index 1
