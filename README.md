# Chinese Checkers

A desktop Chinese checkers game built by **Megan Ying** for Carnegie Mellon University's **15-112: Fundamentals of Programming and Computer Science**, Fall 2021.

[Watch the demo](https://youtu.be/EQbkK0stQs8)

## Features

- Single-player mode against an AI opponent
- Local multiplayer for 2, 4, or 6 players
- Single-step moves and chained jumps
- Highlighted legal moves and single-player hints
- Animated pieces, 30-second turns, and win detection

## Run locally

Use Python 3 with Tkinter and a desktop display. The original project was developed in 2021; Python 3.9 is the original environment recorded in the project files.

```bash
python3 -m pip install -r requirements.txt
python3 mying_term_project.py
```

Keep `cmu_112_graphics.py` in the same folder as the game. To check whether Tkinter is available, run `python3 -m tkinter`; it should open a small window. If Tkinter is missing, install the Tkinter package for your Python distribution (for example, `python3-tk` on Ubuntu).

## How to play

1. Enter **1**, **2**, **4**, or **6** when prompted for the number of players. Choose **1** to play against the computer.
2. Click one of the current player's pieces, then click a highlighted destination.
3. Move to an adjacent empty spot or jump over a neighboring piece into an empty spot. A jumping piece can continue with additional legal jumps.
4. Click the selected piece to finish a chain of jumps. Turns also advance when the 30-second timer expires.
5. Move all ten of your pieces into the opposite triangle to win.

Use **Hint** during your turn in single-player mode, or **Start a new game** to restart.

## Files and attribution

- `mying_term_project.py` — original game implementation by Megan Ying.
- `cmu_112_graphics.py` — bundled CMU 15-112 graphics framework; its original comments and attribution are preserved.
- `requirements.txt` — dependencies used by the bundled graphics framework.

The game originated as a 2021 term project. The development branch adds corrected simulated-state move generation, complete AI jump chains, mid-jump hints, and improved search and evaluation. Earlier milestone submissions, generated Python caches, and duplicate archives are omitted.

## AI and search

The AI searches three complete turns ahead. Breadth-first jump exploration finds every reachable destination and keeps a shortest legal hop sequence for animation. A turn may end at any reachable landing; loops back to the starting position are excluded.

The evaluation prioritizes wins and losses, then scores distinct piece-to-target assignments using hex-grid distance, target occupancy, and the farthest piece from its goal. Distance is a positional heuristic rather than an exact number of turns, since jumps can cross several cells.

Alpha-beta pruning, progress-based move ordering, and a per-search transposition table reduce repeated work. Cached cutoff results retain their lower/upper bound type. Recursive moves are applied and undone on a private board copy.

During a human jump chain, hints consider only the selected piece's remaining jumps or ending the turn. A multi-hop recommendation highlights its next hop.

## Tests

The tests use Python's standard library and load game callbacks without opening a GUI:

```bash
python3 -m unittest discover -s tests -v
```

Coverage includes simulated-state jumps, full-turn paths and animation callbacks, mid-jump hints, all six target triangles, assignment costs checked against brute force, and optimized search compared with exhaustive minimax.
