import time
from card import Card
from predict import simulate_win_rate


def test_simulate_win_rate_accuracy():
    # Pocket aces should have high winrate heads-up
    hand = [Card('s', 14), Card('h', 14)]
    _, _, winrate = simulate_win_rate(hand, [], 2)
    assert winrate > 0.7


def test_simulate_win_rate_speed():
    hand = [Card('s', 14), Card('h', 14)]
    start = time.time()
    simulate_win_rate(hand, [], 3)
    elapsed = time.time() - start
    assert elapsed < 3.0, f"Simulation took {elapsed:.1f}s, should be under 3s"
