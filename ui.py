from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from rich.text import Text

console = Console()

def get_suit_style(suit):
    styles = {
        's': "bold blue",      # Spades
        'h': "bold red",       # Hearts
        'c': "bold green",     # Clubs
        'd': "bold magenta"    # Diamonds
    }
    return styles.get(suit, "white")

def get_suit_symbol(suit):
    symbols = {
        's': "♠",
        'h': "♥",
        'c': "♣",
        'd': "♦"
    }
    return symbols.get(suit, suit)

def render_cards(cards):
    """
    Returns a Text object with colored cards
    """
    text = Text()
    face = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    
    for i, card in enumerate(cards):
        val = face.get(card.value, str(card.value))
        suit_sym = get_suit_symbol(card.suit)
        style = get_suit_style(card.suit)
        
        card_text = Text(f"{val}{suit_sym}", style=style)
        text.append(card_text)
        if i < len(cards) - 1:
            text.append(" ")
            
    return text

def display_header(round_num):
    console.print(Panel(f"[bold cyan]Texas Poker - Round {round_num}[/bold cyan]", box=box.DOUBLE, expand=False))

def display_table(community_cards, pot, current_bet, round_name):
    # Create layout or just panels
    comm_text = render_cards(community_cards) if community_cards else Text("Waiting...", style="dim")
    
    grid = Table.grid(expand=True)
    grid.add_column(justify="center")
    grid.add_row(f"[bold yellow]ROUND: {round_name}[/bold yellow]")
    grid.add_row(Panel(comm_text, title="Community Cards", border_style="green"))
    grid.add_row(f"Pot: [bold gold1]{pot}[/bold gold1] | Current Bet: [bold cyan]{current_bet}[/bold cyan]")
    
    console.print(Panel(grid, title="Table", border_style="white"))

def display_players(players, active_player_idx=None, user_winrate=None):
    table = Table(title="Players", box=box.ROUNDED)
    table.add_column("Pos", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Chips", justify="right", style="green")
    table.add_column("Bet (Round)", justify="right")
    table.add_column("Total (Hand)", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Hand", justify="left")

    for i, p in enumerate(players):
        # Determine status
        status = []
        if p.folded:
            status.append("[dim red]Folded[/dim red]")
        elif p.is_all_in:
            status.append("[bold red]ALL-IN[/bold red]")
        elif active_player_idx is not None and i == active_player_idx:
             status.append("[bold yellow]Act...[/bold yellow]")
        
        status_str = ", ".join(status) if status else "Active"
        
        # Show hand only for user or if showdown (controlled by caller logic really, 
        # but here we assume p.hand is visible if p is human or we are in debug/showdown)
        # For this CLI game, usually human sees own hand. AI hands hidden unless Showdown.
        # But to keep it simple, we render what's passed.
        # IF ai player hand is passed, we render it. In game_loop we sort of leaked it via print.
        # Let's make it mimic real game: only show Human hand.
        
        hand_render = render_cards(p.hand)
        if not p.is_human and not p.hand: # if hand is empty/hidden
             hand_render = Text("XX XX", style="dim")
        
        table.add_row(
            p.position,
            p.name + (" (You)" if p.is_human else ""),
            str(p.chips),
            str(p.current_bet),
            str(p.total_bet_this_hand),
            status_str,
            hand_render
        )

    console.print(table)
    if user_winrate:
         console.print(f"[dim]Estimated Winrate: {user_winrate:.2%}[/dim]", justify="center")


def display_action_log(message):
    console.print(f"[dim]{message}[/dim]")

def input_prompt(prompt_text):
    return console.input(f"[bold yellow]{prompt_text}[/bold yellow]")
