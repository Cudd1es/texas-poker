from player import Player
from game_loop import resolve_pots


def test_side_pot_basic():
    # Scenario: A(10 all-in), B(50 all-in), C(50 cover)
    p1 = Player("A", 0)
    p1.total_bet_this_hand = 10

    p2 = Player("B", 0)
    p2.total_bet_this_hand = 50

    p3 = Player("C", 0)
    p3.total_bet_this_hand = 50

    players = [p1, p2, p3]
    pots = resolve_pots(players)

    # Pot 0 (Main): 30 (10 from each). Eligible: A, B, C
    # Pot 1 (Side): 80 (40 from B, 40 from C). Eligible: B, C
    assert len(pots) == 2
    assert pots[0]['amount'] == 30
    assert "A" in [p.name for p in pots[0]['eligible_players']]
    assert pots[1]['amount'] == 80
    assert "A" not in [p.name for p in pots[1]['eligible_players']]


def test_side_pot_fold():
    # Scenario: A(10 all-in), B(50 folded), C(50 call)
    p1 = Player("A", 0)
    p1.total_bet_this_hand = 10

    p2 = Player("B", 0)
    p2.total_bet_this_hand = 50
    p2.folded = True

    p3 = Player("C", 0)
    p3.total_bet_this_hand = 50

    players = [p1, p2, p3]
    pots = resolve_pots(players)

    # Level 10: 30. Eligible: A, C (B folded)
    # Level 50: 80. Eligible: C only
    assert len(pots) == 2
    assert pots[0]['amount'] == 30
    assert "B" not in [p.name for p in pots[0]['eligible_players']]
    assert pots[1]['amount'] == 80
    assert len(pots[1]['eligible_players']) == 1
    assert pots[1]['eligible_players'][0].name == "C"
