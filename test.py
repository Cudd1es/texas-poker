from card import Card

hand1 = [Card('s', 5), Card('d', 6),Card('s', 6),Card('s', 8),Card('d', 9),Card('h', 10), Card('c', 6)]

print(f"hand1: {hand1}")
print(sorted(hand1))
print(sorted(set(hand1)))