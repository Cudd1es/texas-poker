from math import floor
from deck import create_deck, shuffle_deck, deal_card
from player import HumanPlayer, AIPlayer
from poker_hand import evaluate_hand, compare_hands
from predict import simulate_win_rate
import ui

MAX_ROUNDS = 100

def main():
    players = [
        HumanPlayer("p1", position='SB'),
        AIPlayer("p2", position='BB'),
        AIPlayer("p3", position='-')
    ]

    round_num = 1
    while sum(p.chips > 0 for p in players) > 1 and round_num < MAX_ROUNDS:
        ui.display_header(round_num)

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
            # No print, UI will show

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

            active_players = [p for p in alive_players if not p.folded and not p.is_all_in]
            
            # Show table state
            ui.display_table(community_cards, pot, current_bet, round_name)
            ui.display_players(alive_players)

            if len(active_players) <= 1 and r > 0 and len([p for p in alive_players if not p.folded]) == 1:
                # If only one player left unfolded, skip to end
                break
                
            # betting round
            pot = betting_round(alive_players, community_cards, pot, round_name)
            
            # Update table after betting
            ui.display_table(community_cards, pot, current_bet, round_name)

        unfolded_players = [p for p in alive_players if not p.folded]
        # fold check
        if len(unfolded_players) == 1:
            winner = unfolded_players[0]
            ui.display_action_log(f"Winner: {winner.name} (Others Folded)")
            winner.chips += pot
            ui.display_action_log(f"{winner.name} wins {pot} chips")
        else:
            # Showdown
            all_pots = resolve_pots(alive_players)
            
            # evaluate hands
            player_hands_eval = {}
            for player in alive_players:
                if not player.folded:
                    full_hand = player.hand + community_cards
                    rank, val = evaluate_hand(full_hand)
                    player_hands_eval[player] = {'rank': rank, 'val': val, 'full_hand': full_hand}

            ui.console.print("\n[bold]--- Showdown ---[/bold]")
            for i, pot_obj in enumerate(all_pots):
                pot_amount = pot_obj['amount']
                eligible = pot_obj['eligible_players']
                
                if not eligible: continue
                
                if len(eligible) == 1:
                    winners = [eligible[0]]
                    winning_rank = "Default"
                else:
                    eligible_hands = [player_hands_eval[p]['full_hand'] for p in eligible]
                    idx_winners, winning_rank, _ = compare_hands(eligible_hands)
                    winners = [eligible[idx] for idx in idx_winners]

                cnt_winners = len(winners)
                win_amount = floor(pot_amount / cnt_winners)
                leftover = pot_amount - win_amount * cnt_winners
                
                ui.console.print(f"[bold cyan]Pot {i+1}: {pot_amount}[/bold cyan] -> Winner: {[w.name for w in winners]} ({winning_rank})")
                for w in winners:
                    w.chips += win_amount
                
                if leftover > 0:
                    winners[0].chips += leftover

        ui.display_players(alive_players)
        ui.input_prompt("Press Enter to continue...")
        round_num += 1

    ui.console.print("\n[bold red]GAME OVER[/bold red]")


def betting_round(players, community_cards, pot, round_name):
    current_bet = 0
    # reset round bet
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
        player = players[player_idx % num_players]
        
        # skip inactive
        if player.folded or player.is_all_in or player.chips == 0:
            acted[player] = True
            player_idx += 1
            continue

        # calculate winrate only for human or active ai
        ui.display_table(community_cards, pot, current_bet, round_name)
        
        # We need to simulate winrate to pass to ask_bet
        _, _, winrate = simulate_win_rate(player.hand, community_cards, num_players)
        
        ui.display_players(players, active_player_idx=player_idx % num_players, user_winrate=winrate if player.is_human else None)

        if player.is_human:
             # Human input handling is inside ask_bet, but we need to intercept prompt?
             # No, ask_bet uses input(). We should patch player.py or just let it use standard input 
             # but we can improve the prompt text.
             # Ideally we pass a UI callback to ask_bet, or modify ask_bet.
             # For now, let's just let ask_bet run, it uses input().
             pass 
        else:
             ui.display_action_log(f"{player.name} is thinking...")

        flag, bet = player.ask_bet(current_bet, winrate)
        
        if flag == 1: # raise/call/check
            pot += bet
            if player.current_bet > current_bet:
                current_bet = player.current_bet
                last_raiser_idx = player_idx % num_players
                acted = {p: False for p in players}
                ui.display_action_log(f"{player.name} Raised to {current_bet}")
            else:
                ui.display_action_log(f"{player.name} Called/Checked")
            acted[player] = True
        elif flag == -1: # fold
            ui.display_action_log(f"{player.name} Folded")
            acted[player] = True
        elif flag == 0: # all in
            pot += bet
            if player.current_bet > current_bet:
                current_bet = player.current_bet
                last_raiser_idx = player_idx % num_players
                acted = {p: False for p in players}
            ui.display_action_log(f"{player.name} went ALL-IN!")
            acted[player] = True

        if all(p.folded or p.is_all_in or p.current_bet == current_bet for p in players):
            if last_raiser_idx is None:
                if all(acted[p] for p in players):
                    break
            elif acted[players[last_raiser_idx]]:
                break

        player_idx += 1
        
    return pot

def resolve_pots(players):
    """
    Calculate main pot and side pots based on players' total contribution.
    Returns a list of dicts: [{'amount': int, 'eligible_players': [Player]}]
    """
    pots = []
    # contributions stores {player: total_bet}
    contributions = {p: p.total_bet_this_hand for p in players if p.total_bet_this_hand > 0}
    if not contributions:
        return []

    # get sorted unique betting levels
    levels = sorted(list(set(contributions.values())))
    
    last_level = 0
    for level in levels:
        pot_amount = 0
        eligible_players = []
        
        # calculate contribution for this level
        for p, bet in contributions.items():
            if bet > last_level:
                contribution = min(bet, level) - last_level
                pot_amount += contribution
                if not p.folded:
                    eligible_players.append(p)
        
        if pot_amount > 0 and eligible_players:
            pots.append({
                'amount': pot_amount,
                'eligible_players': eligible_players
            })
        
        last_level = level

    return pots

if __name__ == "__main__":
    main()