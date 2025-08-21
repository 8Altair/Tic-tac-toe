# Tic-Tac-Toe

A simple Tic-Tac-Toe GUI application written in Python. The primary goal of this project is to implement and demonstrate an AI opponent using 
the Minimax algorithm, with an optional alpha–beta pruning optimization. The focus is on the algorithmic implementation, not on delivering a 
polished or particularly entertaining gameplay experience.

The application can be run easily using the included Windows executable (`XO.exe`).

## Features

- GUI built with Tkinter and CustomTkinter
- Play as X or O against the computer
- AI opponent powered by Minimax, with optional alpha–beta pruning
- Difficulty levels from 1 (easy) to 9 (hard)
- Automatic detection of win, loss, or draw

## Getting Started

You can run the game in either of the following ways.

### Option 1: Windows executable (recommended)
Double-click `XO.exe` to start the game. No Python installation is required.

### Option 2: Run from source
1) Ensure you have Python 3 installed.  
2) Install the required package: CustomTkinter.  
3) Run the main script.

## How to Play

1) Launch the game using `XO.exe` or by running `main.py`.  
2) Choose whether to play as X or O.  
3) Select the AI algorithm (Minimax or Alpha-Beta).  
4) Pick a difficulty level from 1 to 9.  
5) Click “Start Game” to begin.  
6) Click an empty square to place your mark; the AI will respond with its move.  
7) The game announces the result when a player wins or when the board is full (draw).  
8) Use “Restart” to set up a new game at any time.

The rules follow standard Tic-Tac-Toe. The interface is intentionally simple and intuitive.

## AI Overview

- The computer opponent uses the Minimax algorithm to evaluate moves.  
- Alpha–beta pruning (optional in the GUI) speeds up Minimax by pruning branches that cannot affect the final decision; it does not change the outcome quality.  
- Difficulty levels may introduce reduced look-ahead and/or slight randomness at lower settings, while the highest difficulty aims to play optimally.

Details of the AI, including scoring and search behavior, are documented via docstrings in the code (see `algorithm_functions.py`).

## Project Structure

- `main.py` – Application entry point and GUI wiring (menus, board, interactions)
- `algorithm_functions.py` – AI logic (Minimax and optional alpha–beta pruning) and move selection helpers
- `game_functions.py` – Game utilities (board evaluation, win/tie checks, available moves)
- `XO.exe` – Prebuilt Windows executable for running the game without Python

## Notes

- This repository is intended as an AI demonstration. The user interface is minimal by design.
- If you encounter issues with icons or platform specifics when running from source, ensure you are using a recent Python 3 release and have installed CustomTkinter.
