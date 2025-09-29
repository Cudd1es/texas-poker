from math import floor
from deck import create_deck, shuffle_deck, deal_card, sort_hand
from player import Player, HumanPlayer, AIPlayer
from poker_hand import evaluate_hand, compare_hands
from predict import simulate_win_rate

MAX_ROUNDS = 100

def main():
    players = [
        HumanPlayer("p1", position='SB'),
        HumanPlayer("p2", position='BB'),
        AIPlayer("p3", position='-')
    ]

    round_num = 1
    while sum(p.chips > 0 for p in players) > 1 and round_num < MAX_ROUNDS:
        print(f'\n\n ======== [Round {round_num}] ========')

        # reset players
        for p in players:
            p.reset_for_new_round()
        alive_players = [p for p in players if p.chips > 0]

        # deal deck
        deck = create_deck()
        shuffle_deck(deck)
        hands, deck = deal_card(deck, num_players=len(alive_players))
        for i, player in enumerate(alive_players):
            player.hand = hands[i]
            #debug
            print(f"player {player.name} hand: {' '.join([c.to_colored_str() for c in player.hand])}")
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

            active_players = [p for p in alive_players if not p.folded and not p.is_all_in]
            if len(active_players) == 1:
                print("only one player left, skipping.")
                break

            for player in alive_players:
                if player.folded or player.is_all_in:
                    continue
                print(f"player {player.name} hand: {' '.join([c.to_colored_str() for c in player.hand])}, community cards: {' '.join([c.to_colored_str() for c in community_cards])}")
                # add prediction
                _, _, winrate = simulate_win_rate(player.hand, community_cards, len(alive_players))
                print(f"current winrate: {winrate}")

                flag, bet = player.ask_bet(current_bet, winrate)
                if flag == 1:
                    print(f"player {player.name} bet: {bet}")
                    pot += bet
                elif flag == -1:
                    print(f"player {player.name} has folded")
                elif flag == 0:
                    print(f"player {player.name} is all in")
                    pot += bet
                current_bet = max(current_bet, bet)
                #debug
                print(f"####DEBUG: player {player.name}: chips: {player.chips}")
                #!debug
        unfolded_players = [p for p in alive_players if not p.folded]
        # fold check
        if len(unfolded_players) == 1:
            winner = unfolded_players[0]
            print(f"player {winner.name} wins as all others folded")
            winner.chips += pot
            print(f"{winner.name} wins {pot} chips")
            print(f"current chips: {winner.chips}")
        else:
            # normal compare
            player_hands = []
            existing_players = []
            for player in alive_players:
                if not player.folded:
                    player_hand = player.hand + community_cards
                    player_hands.append(player_hand)
                    existing_players.append(player)
                    highest_hand = evaluate_hand(player_hand)
                    print(f"player {player.name} hand: {' '.join([c.to_colored_str() for c in player_hand])}, highest hand: {highest_hand}")

            if player_hands:
                winners, winning_rank, winning_points = compare_hands(player_hands)
                #print(f"winners: {winners}, winning rank: {winning_rank}, winning points: {winning_points}")
                cnt_winners = len(winners)
                winning_chips = floor(pot / cnt_winners)
                leftover = pot - winning_chips * cnt_winners
                print("winner:")
                for idx in winners:
                    winner = existing_players[idx]
                    print(f"{winner.name} wins {winning_chips} chips")
                    winner.chips += winning_chips
                    print(f"current chips: {winner.chips}")
                print(f"winning rank: {winning_rank}, {winning_points}")
                if leftover > 0:
                    existing_players[winners[0]].chips += leftover

        print(f"=== Chips after round ===")
        for p in players:
            print(f"{p.name} chips: {p.chips}")
        round_num += 1

    print("\n ==== over ====")
    print("final chips:")
    for p in players:
        print(f"{p.name} chips: {p.chips}")



if __name__ == "__main__":
    main()