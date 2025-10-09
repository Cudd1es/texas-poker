from math import floor
from deck import create_deck, shuffle_deck, deal_card
from player import HumanPlayer, AIPlayer
from poker_hand import evaluate_hand, compare_hands
from predict import simulate_win_rate

MAX_ROUNDS = 100

def main():
    players = [
        HumanPlayer("p1", position='SB'),
        AIPlayer("p2", position='BB'),
        AIPlayer("p3", position='-')
    ]

    round_num = 1
    while sum(p.chips > 0 for p in players) > 1 and round_num < MAX_ROUNDS:
        print(f'\n\n======== [Round {round_num}] ========')

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

            print()
            print("="*8 + f" round: {round_name} " + "="*8)
            print(f"pot: {pot}, current_bet: {current_bet}")
            #print(f"current bet: {current_bet}")
            print(f"community cards: {' '.join([c.to_colored_str() for c in community_cards])}")
            print("="*16)

            active_players = [p for p in alive_players if not p.folded and not p.is_all_in]
            if len(active_players) == 1:
                print("only one player left, skipping.")
                break
            # betting round
            pot = betting_round(alive_players, community_cards, pot, round_name)

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

def betting_round(players, community_cards, pot, round_name):
    print(f"\n==== {round_name} ====")
    current_bet = 0
    for player in players:
        player.current_bet = 0
    num_players = len(players)
    last_raiser_idx = None
    acted = {p: False for p in players}
    player_idx = 0

    active_players = [p for p in players if not p.folded and not p.is_all_in and p.chips > 0]
    if len(active_players) <= 1:
        return pot

    while True:
        # skip all in / fold
        player = players[player_idx % num_players]
        if player.folded or player.is_all_in or player.chips == 0:
            acted[player] = True
            player_idx += 1
            continue

        # predict winrate
        print(f"your hand: {' '.join([c.to_colored_str() for c in player.hand])}, community cards: {' '.join([c.to_colored_str() for c in community_cards])}")
        _, _, winrate = simulate_win_rate(player.hand, community_cards, num_players)
        if not player.is_human:
            print(f"current winrate: {winrate}")
        flag, bet = player.ask_bet(current_bet, winrate)
        if flag == 1: # raise/call/check
            print(f"player {player.name} bet: {bet}")
            pot += bet
            if player.current_bet > current_bet:
                current_bet = player.current_bet
                last_raiser_idx = player_idx % num_players
                acted = {p: False for p in players}
            acted[player] = True
        elif flag == -1: # fold
            print(f"player {player.name} has folded")
            acted[player] = True
        elif flag == 0: # all in
            print(f"player {player.name} is all in")
            pot += bet
            if player.current_bet > current_bet:
                current_bet = player.current_bet
                last_raiser_idx = player_idx % num_players
                acted = {p: False for p in players}
            acted[player] = True

        # debug
        # print(f"current bet {current_bet}")
        # for p in players:
        #    print(f"{p.name} , {p.current_bet}, acted: {acted[p]}")
        # print(f"last raiser idx: {last_raiser_idx}")
        # if last_raiser_idx is not None:
        #    print (f"{acted[players[last_raiser_idx]]}")
        # !debug
        if all(p.folded or p.is_all_in or p.current_bet == current_bet for p in players):
            if last_raiser_idx is None:
                if all(acted[p] for p in players):
                    break
            elif acted[players[last_raiser_idx]]:
                break

        player_idx += 1
    return pot


if __name__ == "__main__":
    main()