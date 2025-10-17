# Texas Hold'em Poker Engine

A modular Python implementation of a Texas Hold'em poker engine supporting human and AI players, betting rounds, hand evaluation, and win-rate simulation.

## Features

- Full Texas Hold'em game flow (deal, betting rounds, community cards, showdown)
- Human and AI players (AI uses basic win-rate simulation for betting decisions)
- Modular code structure for easy extension and testing
- No external dependencies, pure Python

## Project Structure

```
deck.py         # Deck construction, shuffle, and dealing
card.py         # Card class and display
player.py       # Human and AI player classes and betting logic
game_loop.py    # Main game loop and betting round management
poker_hand.py   # Hand evaluation and comparison
predict.py      # Win-rate simulation (Monte Carlo)
```

## Quick Start

**Requirements:**

- Python 3.8+

**Run the game:**

```bash
python game_loop.py
```

The game runs in the terminal and supports both human and AI players.

## Example

```
======== [Round 1] ========
player p1 hand: Ah Qd
player p2 hand: 8c 7d
player p3 hand: 3h 9s

========= round: Flop =========
pot: 0, current_bet: 0
community cards: 2d 9h Jc

p1, enter the bet for this round ('c' to call, 'k' to check, 'a' to all in, 'f' to fold): k
...
winner: p3 wins 1500 chips
```

## License

MIT License

