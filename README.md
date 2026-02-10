# Texas Hold'em Poker Engine

A modular Python implementation of a Texas Hold'em poker engine supporting human and AI players, betting rounds, hand evaluation, and win-rate simulation.

## Features

- Full Texas Hold'em game flow (deal, betting rounds, community cards, showdown)
- Human and AI players (AI uses Monte Carlo win-rate simulation for betting decisions)
- Rich terminal UI with colored cards and table display
- Side pot calculation for all-in scenarios
- Modular code structure for easy extension and testing

## Project Structure

```
card.py         # Card class and display
deck.py         # Deck construction, shuffle, and dealing
player.py       # Human and AI player classes and betting logic
game_loop.py    # Main game loop and betting round management
poker_hand.py   # Hand evaluation and comparison
predict.py      # Win-rate simulation (Monte Carlo)
ui.py           # Rich-based terminal UI
tests/          # Test suite (pytest)
```

## Quick Start

**Requirements:**

- Python 3.8+

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Run the game:**

```bash
python game_loop.py
```

The game runs in the terminal and supports both human and AI players.

**Run tests:**

```bash
pytest tests/ -v
```

## Example

```
======== [Round 1] ========
player p1 hand: Ah Qd
player p2 hand: XX XX
player p3 hand: XX XX

========= round: Flop =========
pot: 0, current_bet: 0
community cards: 2d 9h Jc

p1, enter the bet for this round ('c' to call, 'k' to check, 'a' to all in, 'f' to fold): k
...
winner: p3 wins 1500 chips
```

## License

MIT License
