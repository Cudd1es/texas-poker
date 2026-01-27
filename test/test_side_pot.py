import sys
sys.path.append('..')
from player import Player
from game_loop import resolve_pots

def test_side_pot_basic():
    # Scenario 1: Basic Side Pot
    # A: 10 (All-in)
    # B: 50 (All-in)
    # C: 100 (Cover) - Bets 50 to match B
    
    p1 = Player("A", 0)
    p1.total_bet_this_hand = 10
    
    p2 = Player("B", 0)
    p2.total_bet_this_hand = 50
    
    p3 = Player("C", 0)
    p3.total_bet_this_hand = 50 # C covers B
    
    players = [p1, p2, p3]
    pots = resolve_pots(players)
    
    print("\n--- Test Scenario 1: Basic Side Pot ---")
    for i, pot in enumerate(pots):
        names = [p.name for p in pot['eligible_players']]
        print(f"Pot {i}: Amount={pot['amount']}, Eligible={names}")

    # Expected:
    # Pot 0 (Main): 30 (10 from A, 10 from B, 10 from C). Eligible: A, B, C
    # Pot 1 (Side): 80 (40 from B, 40 from C). Eligible: B, C
    
    assert len(pots) == 2
    assert pots[0]['amount'] == 30
    assert "A" in [p.name for p in pots[0]['eligible_players']]
    assert pots[1]['amount'] == 80
    assert "A" not in [p.name for p in pots[1]['eligible_players']]
    print("✅ Scenario 1 Passed")

def test_side_pot_fold():
    # Scenario 2: Folded Player Money
    # A: 10 (All-in)
    # B: 50 (Folded)
    # C: 50 (Call)
    
    p1 = Player("A", 0)
    p1.total_bet_this_hand = 10
    
    p2 = Player("B", 0)
    p2.total_bet_this_hand = 50
    p2.folded = True
    
    p3 = Player("C", 0)
    p3.total_bet_this_hand = 50
    
    players = [p1, p2, p3]
    pots = resolve_pots(players)
    
    print("\n--- Test Scenario 2: Folded Player ---")
    for i, pot in enumerate(pots):
        names = [p.name for p in pot['eligible_players']]
        print(f"Pot {i}: Amount={pot['amount']}, Eligible={names}")

    # Expected:
    # Level 10: A(10) + B(10) + C(10) = 30. Eligible: A, C. (B folded)
    # Level 50: B(40) + C(40) = 80. Eligible: C. (A maxed out, B folded)
    
    assert len(pots) == 2
    assert pots[0]['amount'] == 30
    assert "B" not in [p.name for p in pots[0]['eligible_players']]
    assert pots[1]['amount'] == 80
    assert len(pots[1]['eligible_players']) == 1 and pots[1]['eligible_players'][0].name == "C"
    print("✅ Scenario 2 Passed")

if __name__ == "__main__":
    test_side_pot_basic()
    test_side_pot_fold()
