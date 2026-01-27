# Texas Hold'em Poker Engine

A modular Python implementation of a Texas Hold'em poker engine featuring advanced rules (Side Pots), rich terminal UI, and AI simulation.

## Features

- **Full Texas Hold'em Rules**: Supports deal, betting rounds, community cards, and showdown.
- **Advanced Side Pot Logic**: Correctly handles multi-way All-in scenarios with uneven stacks and main/side pot splits.
- **Robust Hand Evaluation**: Accurate detection of all poker hands, including correct handling of **Wheel Straights (A-2-3-4-5)** and complex Full Houses.
- **Rich Terminal UI**: Beautiful command-line interface powered by the `rich` library, featuring colored cards, tables, and panels.
- **AI Players**: AI opponents that use Monte Carlo simulation to estimate win rates and make betting decisions.
- **Modular Design**: Clean separation of concerns for easy extension.

## Project Structure

```
deck.py             # Deck construction, shuffle, and dealing
card.py             # Card class with suit/value logic
player.py           # Human and AI player classes and state tracking
game_loop.py        # Main game loop, betting, and pot resolution
poker_hand.py       # Hand evaluation and comparison logic
predict.py          # Win-rate simulation (Monte Carlo)
ui.py               # UI rendering module (Rich)
test/               # Unit tests
```

## Quick Start

**Requirements:**
- Python 3.8+
- `rich` library

**Installation:**

Recommended to use a virtual environment (e.g., conda):

```bash
conda create -n texas python=3.13
conda activate texas
pip install rich
```

**Run the Game:**

```bash
python game_loop.py
```

## Testing

The project includes a suite of tests to verify game logic, including the recent fixes for Straights and Side Pots.

```bash
cd test
python3 test_fixes.py      # Verify hand evaluation logic
python3 test_side_pot.py   # Verify main/side pot distribution
```

## Example UI

The game now features a modernized TUI:

```
╭─────────────────────────────────────────────────────────────────────────────────────────────────── Table ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                            ROUND: Flop                                                            │
│ ╭─────────────────────────────────────────────────────── Community Cards ───────────────────────────────────────────────────────╮ │
│ │                                                          K♠ 10♥ 2♦                                                            │ │
│ ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│                                                   Pot: 150 | Current Bet: 50                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## License

MIT License
