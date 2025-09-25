from math import floor

from deck import create_deck, shuffle_deck, deal_card, sort_hand
from player import Player
from poker_hand import evaluate_hand, compare_hands

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
            #debug
            print(f"####DEBUG: player {player.name}: chips: {player.chips}")
            #!debug
    player_hands = []
    for player in players:
        player_hand = player.hand + community_cards
        player_hands.append(player_hand)
        highest_hand = evaluate_hand(player_hand)
        print(f"player {player.name} hand: {' '.join([c.to_colored_str() for c in player_hand])}, highest hand: {highest_hand}")

    winners, winning_rank, winning_points = compare_hands(player_hands)
    print(f"winners: {winners}, winning rank: {winning_rank}, winning points: {winning_points}")

    cnt_winners = len(winners)
    winning_chips = floor(pot / cnt_winners)
    print("winner:")
    for winner in winners:
        print(f"{players[winner].name} wins {winning_chips} chips")
        players[winner].chips += winning_chips
        print(f"current chips: {players[winner].chips}")
    print(f"winning rank: {winning_rank}, {winning_points}")



if __name__ == "__main__":
    main()