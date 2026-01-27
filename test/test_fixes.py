import sys
sys.path.append('..')
from card import Card
from poker_hand import evaluate_hand

def test_wheel_straight():
    # A, 2, 3, 4, 5
    cards = [
        Card('s', 14),
        Card('d', 2),
        Card('h', 3),
        Card('c', 4),
        Card('s', 5),
        Card('d', 9), # kicker
        Card('h', 10) # kicker
    ]
    rank, values = evaluate_hand(cards)
    print(f"Wheel Hand: {rank}, {values}")
    assert rank == "Straight"
    assert values == [5, 4, 3, 2, 1]

def test_dual_trips_full_house():
    # AAA KKK Q -> Full House, chips AAA, pair KKK
    cards = [
        Card('s', 14), Card('d', 14), Card('h', 14),
        Card('s', 13), Card('d', 13), Card('h', 13),
        Card('c', 12)
    ]
    rank, values = evaluate_hand(cards)
    print(f"Dual Trips Hand: {rank}, {values}")
    assert rank == "Full House"
    assert values == [14, 13]

def test_standard_full_house():
    # AAA KK Q J -> Full House
    cards = [
        Card('s', 14), Card('d', 14), Card('h', 14),
        Card('s', 13), Card('d', 13),
        Card('c', 12), Card('d', 11)
    ]
    rank, values = evaluate_hand(cards)
    print(f"Standard Full House: {rank}, {values}")
    assert rank == "Full House"
    assert values == [14, 13]

def test_card_sort():
    c1 = Card('s', 10)
    c2 = Card('h', 10)
    # in deck.py: suit_order = {'s':0, 'h':1, 'c':2, 'd':3}
    # card.py new sort: s < h.
    assert c1 < c2
    print(f"Card Sort: {c1} < {c2} is {c1 < c2}")

if __name__ == "__main__":
    try:
        test_wheel_straight()
        print("✅ test_wheel_straight passed")
    except AssertionError as e:
        print(f"❌ test_wheel_straight failed: {e}")
        
    try:
        test_dual_trips_full_house()
        print("✅ test_dual_trips_full_house passed")
    except AssertionError as e:
        print(f"❌ test_dual_trips_full_house failed: {e}")

    try:
        test_standard_full_house()
        print("✅ test_standard_full_house passed")
    except AssertionError as e:
        print(f"❌ test_standard_full_house failed: {e}")

    try:
        test_card_sort()
        print("✅ test_card_sort passed")
    except AssertionError as e:
        print(f"❌ test_card_sort failed: {e}")
