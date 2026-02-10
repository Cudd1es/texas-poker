from card import Card
from poker_hand import evaluate_hand


def test_wheel_straight():
    # A, 2, 3, 4, 5
    cards = [
        Card('s', 14), Card('d', 2), Card('h', 3),
        Card('c', 4), Card('s', 5), Card('d', 9), Card('h', 10)
    ]
    rank, values = evaluate_hand(cards)
    assert rank == "Straight"
    assert values == [5, 4, 3, 2, 14]


def test_dual_trips_full_house():
    # AAA KKK Q -> Full House, trips AAA, pair KKK
    cards = [
        Card('s', 14), Card('d', 14), Card('h', 14),
        Card('s', 13), Card('d', 13), Card('h', 13), Card('c', 12)
    ]
    rank, values = evaluate_hand(cards)
    assert rank == "Full House"
    assert values == [14, 13]


def test_standard_full_house():
    # AAA KK Q J -> Full House
    cards = [
        Card('s', 14), Card('d', 14), Card('h', 14),
        Card('s', 13), Card('d', 13), Card('c', 12), Card('d', 11)
    ]
    rank, values = evaluate_hand(cards)
    assert rank == "Full House"
    assert values == [14, 13]


def test_card_sort():
    c1 = Card('s', 10)
    c2 = Card('h', 10)
    # suit order: s < h < c < d
    assert c1 < c2
