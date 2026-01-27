import sys
sys.path.append('..')
from collections import Counter
from poker_hand import evaluate_hand
from card import Card

hand1 = [Card('s', 5), Card('d', 6),Card('s', 6),Card('s', 8),Card('d', 9),Card('h', 10), Card('c', 6)]

print(f"hand1: {hand1}")
print(sorted(hand1))
print(sorted(set(hand1)))


counter = Counter(hand1)
values = [c.value for c in hand1]
c_values = Counter(values)
tmp1 = [v for v, c in c_values.items() if c == 3]
print(f"values: {c_values}")
print(f"tmp1: {tmp1}")


ret = evaluate_hand(hand1)
print(ret)