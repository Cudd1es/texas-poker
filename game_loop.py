from deck import create_deck, shuffle_deck, deal_card, sort_hand
from player import Player

def main():
    player1 = Player('p1', position='SB', is_human = True)
    player2 = Player('p2', position='BB', is_human = True)
    players = [player1, player2]

    deck = create_deck()
    shuffle_deck(deck)
    hands, deck = deal_card(deck, num_players=len(players))
    for i, player in enumerate(players):
        player.hand = hands[i]
        #debug
        print(f"player {i} hand: {' '.join([c.to_colored_str() for c in player.hand])}")
        #!debug
    pot = 0
    current_bet = 0
    community_cards = []
    round_names = ["Pre-flop", "Flop", "Turn", "River"]
    for r, round_name in enumerate(round_names):
        if round_name == "Flop":
            for _ in range(3):
                community_cards.append(deck.pop())
        elif round_name in ["Turn", "River"]:
            community_cards.append(deck.pop())

        print("="*8 + f" round: {round_name} " + "="*8)
        print(f"pot: {pot}")
        print(f"current bet: {current_bet}")
        print(f"community cards: {' '.join([c.to_colored_str() for c in community_cards])}")
        print("="*16)
        for player in players:
            if player.folded or player.is_all_in:
                continue
            print(f"player {player.name} hand: {' '.join([c.to_colored_str() for c in player.hand])}, community cards: {' '.join([c.to_colored_str() for c in community_cards])}")
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