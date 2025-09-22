import random
from card import Card

def create_deck():
    suits = ['s', 'h', 'c', 'd']
    deck = []
    for suit in suits:
        for value in range(2, 15):
            deck.append(Card(suit, value))
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)

def deal_card(deck, num_players = 2):
    hands = [[] for _ in range(num_players)]
    for _ in range(2):
        for i in range(num_players):
            hands[i].append(deck.pop(0))
    return hands, deck

def card_sort_key(card:Card):
    suit_order = {'s':0, 'h':1, 'c':2, 'd':3}
    suit_rank = suit_order[card.suit]
    return card.value, suit_order[card.suit]

def sort_hand(hand:list[Card]):
    return sorted(hand, key=card_sort_key)