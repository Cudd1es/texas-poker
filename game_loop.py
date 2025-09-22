from deck import create_deck, shuffle_deck, deal_card, sort_hand
from player import Player

def main():
    player1 = Player('p1', position='SB', is_human = True)
    player2 = Player('p2', position='BB', is_human = True)
    players = [player1, player2]

    deck = create_deck()
    shuffle_deck(deck)

    hands, deck = deal_card(deck, num_players=2)
    for i, player in enumerate(players):
        player.hand = hands[i]
        #debug
        print(f"player {i} hand: {' '.join([c.to_colored_str() for c in player.hand])}")
        #!debug
    pot = 0
    current_bet = 0
    for player in players:
        flag, bet = player.ask_bet(current_bet)
        if flag == 1:
            print(f"player {player.name} bet: {bet}")
        elif flag == -1:
            print(f"player {player.name} has folded")
        elif flag == 0:
            print(f"player {player.name} is all in")
        current_bet = bet
        pot += bet

if __name__ == "__main__":
    main()