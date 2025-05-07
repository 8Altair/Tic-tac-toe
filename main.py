import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkRadioButton, CTkLabel, CTkOptionMenu

# Initialize dark theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

DIFFICULTY_OPTIONS = tuple(range(1, 10))
WINNING_LINES = \
    (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

BONUS = 11


def has_moves_left(board_state):
    return "-" in board_state


def evaluate_board_state(board_state):
    for a, b, c in WINNING_LINES:
        symbol = board_state[a]
        if symbol == board_state[b] == board_state[c] and symbol != "-":
            return 100 if symbol == "X" else -100

    open_lines_max = 0
    open_lines_min = 0
    two_in_row_max = 0
    two_in_row_min = 0

    for a, b, c in WINNING_LINES:
        line = (board_state[a], board_state[b], board_state[c])
        if "O" not in line:
            open_lines_max += 1
            if line.count("X") == 2:
                two_in_row_max += 1
        if "X" not in line:
            open_lines_min += 1
            if line.count("O") == 2:
                two_in_row_min += 1

    score = (open_lines_max - open_lines_min) + BONUS * (two_in_row_max - two_in_row_min)
    if board_state[4] == "X":
        score += BONUS
    elif board_state[4] == "O":
        score -= BONUS

    return score


def get_ordered_moves(board_state, player):
    candidates = []
    for i in range(len(board_state)):
        if board_state[i] == "-":
            board_state[i] = player
            score = evaluate_board_state(board_state)
            board_state[i] = "-"
            candidates.append((i, score))

    return [i for i, _ in sorted(candidates, key=lambda pair: pair[1], reverse=(player == "X"))]    # For X (maximizer), sort descending; for O (minimizer), ascending



def minimax_search(board_state, current_depth, is_maximizing, alpha, beta, depth_limit):
    score = evaluate_board_state(board_state)
    if score == 100 or score == -100 or current_depth == depth_limit or not has_moves_left(board_state):
        return score

    if is_maximizing:
        best_score = float("-inf")
        for index in get_ordered_moves(board_state, "X"):
            board_state[index] = "X"
            value = minimax_search(board_state, current_depth + 1, False, alpha, beta, depth_limit)
            board_state[index] = "-"
            best_score = max(best_score, value)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_score
    else:
        best_score = float("inf")
        for index in get_ordered_moves(board_state, "O"):
            board_state[index] = "O"
            value = minimax_search(board_state, current_depth + 1, True, alpha, beta, depth_limit)
            board_state[index] = "-"
            best_score = min(best_score, value)
            beta = min(beta, best_score)
            if alpha >= beta:
                break

        return best_score


def minimax_plain(board_state, current_depth, is_maximizing, depth_limit):
    score = evaluate_board_state(board_state)
    if score == 100 or score == -100 or current_depth == depth_limit or not has_moves_left(board_state):
        return score

    if is_maximizing:
        best_score = float("-inf")
        for index in range(len(board_state)):
            if board_state[index] == "-":
                board_state[index] = "X"
                value = minimax_plain(board_state, current_depth + 1, False, depth_limit)
                board_state[index] = "-"
                best_score = max(best_score, value)

        return best_score
    else:
        best_score = float("inf")
        for index in range(len(board_state)):
            if board_state[index] == "-":
                board_state[index] = "O"
                value = minimax_plain(board_state, current_depth + 1, True, depth_limit)
                board_state[index] = "-"
                best_score = min(best_score, value)

        return best_score


def compute_best_move(board_state, player_symbol, depth_limit):
    best_move = -1

    if player_symbol == "X":
        best_value = float("-inf")
    else:
        best_value = float("inf")

    alpha = float("-inf")
    beta = float("inf")
    for index in get_ordered_moves(board_state, player_symbol):
        board_state[index] = player_symbol
        next_is_maximizing = player_symbol == "O"
        move_value = minimax_search(board_state, 0, next_is_maximizing, alpha, beta, depth_limit)
        board_state[index] = "-"
        if (player_symbol == "X" and move_value > best_value) or (player_symbol == "O" and move_value < best_value):
            best_value = move_value
            best_move = index
    return best_move


def compute_best_move_plain(board_state, player_symbol, depth_limit):
    best_move = -1
    best_value = float("-inf") if player_symbol == "X" else float("inf")

    for index in range(len(board_state)):
        if board_state[index] == "-":
            board_state[index] = player_symbol
            next_is_maximizing = player_symbol == "O"
            move_value = minimax_plain(board_state, 0, next_is_maximizing, depth_limit)
            board_state[index] = "-"
            if (player_symbol == "X" and move_value > best_value) or (player_symbol == "O" and move_value < best_value):
                best_value = move_value
                best_move = index
    return best_move


class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.geometry("600x700")
        self.master.resizable(True, True)
        self.human_symbol = None
        self.ai_symbol = None
        self.current_turn = None
        self.max_search_depth = DIFFICULTY_OPTIONS[0]
        self._setup_selection_panel()

    def _setup_selection_panel(self):
        self.selection_frame = CTkFrame(self.master)  # dark‐mode frame :contentReference[oaicite:9]{index=9}
        self.selection_frame.pack(expand=True)

        prompt_label = CTkLabel(self.selection_frame, text="Choose your symbol:", font=("Arial", 24))
        prompt_label.pack(pady=20)

        self.symbol_choice_var = tk.StringVar(value="X")

        radio_x = CTkRadioButton(self.selection_frame, text="Play as X", variable=self.symbol_choice_var,
                                 value="X", font=("Arial", 18), width=150)
        radio_x.pack(pady=5, anchor="w")

        radio_o = CTkRadioButton(self.selection_frame, text="Play as O", variable=self.symbol_choice_var, value="O",
                                 font=("Arial", 18), width=150)
        radio_o.pack(pady=5, anchor="w")

        # Algorithm selector
        algorithm_label = CTkLabel(self.selection_frame, text="Algorithm:", font=("Arial", 18))
        algorithm_label.pack(pady=5, anchor="w")

        self.algorithm_variable = tk.StringVar(value="Alpha-Beta")
        algorithm_menu = CTkOptionMenu(self.selection_frame, variable=self.algorithm_variable, values=["Minimax", "Alpha-Beta"])
        algorithm_menu.pack(pady=5, anchor="w")

        # Difficulty selector
        difficulty_label = CTkLabel(self.selection_frame, text="Difficulty:", font=("Arial", 18))
        difficulty_label.pack(pady=5, anchor="w")

        self.difficulty_variable = tk.StringVar(value=str(self.max_search_depth))
        difficulty_menu = CTkOptionMenu(self.selection_frame, variable=self.difficulty_variable,
                                        values=[str(option) for option in DIFFICULTY_OPTIONS])
        difficulty_menu.pack(pady=5, anchor="w")

        start_button = CTkButton(self.selection_frame, text="Start Game", font=("Arial", 24),
                                 command=self._start_game)
        start_button.pack(pady=20)

    def _start_game(self):
        self.max_search_depth = int(self.difficulty_variable.get())
        self.human_symbol = self.symbol_choice_var.get()
        self.ai_symbol = "O" if self.human_symbol == "X" else "X"
        self.current_turn = "X"
        self.selection_frame.destroy()
        self._setup_game_panel()

        if self.current_turn == self.ai_symbol:
            self.master.after(100, self._execute_ai_move)

    def _setup_game_panel(self):
        self.control_frame = CTkFrame(self.master)  # dark‐mode frame
        self.control_frame.pack(pady=10)

        restart_button = CTkButton(self.control_frame, text="Restart", font=("Arial", 18),
                                   command=self._reset_to_selection)
        restart_button.pack(side="left", padx=10)

        self.board_frame = CTkFrame(self.master)
        self.board_frame.pack(expand=True)

        self.cell_buttons = []
        self.game_board = ["-" for _ in range(9)]

        for index in range(9):
            button = CTkButton(self.board_frame, text="", width=50, height=50, font=("Arial", 48),
                               command=lambda i=index: self._on_cell_clicked(i))
            button.grid(row=index // 3, column=index % 3, padx=5, pady=5)
            self.cell_buttons.append(button)

        self._update_board_ui()

    def _on_difficulty_changed(self, _):
        self.max_search_depth = int(self.difficulty_variable.get())

    def _reset_to_selection(self):
        self.control_frame.destroy()
        self.board_frame.destroy()
        self._setup_selection_panel()

    def _on_cell_clicked(self, index):
        if self.current_turn == self.human_symbol and self.game_board[index] == "-":
            self.game_board[index] = self.human_symbol
            self._update_board_ui()
            if self._check_for_end():
                return
            self.current_turn = self.ai_symbol
            self.master.after(100, self._execute_ai_move)

    def _execute_ai_move(self):
        if self.algorithm_variable.get() == "Minimax":
            best_index = compute_best_move_plain(self.game_board, self.current_turn, self.max_search_depth)
        else:
            best_index = compute_best_move(self.game_board, self.current_turn, self.max_search_depth)

        if best_index != -1:
            self.game_board[best_index] = self.current_turn
            self._update_board_ui()
            if self._check_for_end():
                return
            self.current_turn = self.human_symbol

    def _update_board_ui(self):
        for i, button in enumerate(self.cell_buttons):
            symbol = self.game_board[i]
            if symbol == "-":
                button.configure(text="", state="normal")
            else:
                button.configure(text=symbol, state="disabled")

    def _check_for_end(self):
        winner = self._determine_winner()
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self._reset_to_selection()
            return True
        if not has_moves_left(self.game_board):
            messagebox.showinfo("Game Over", "It’s a tie!")
            self._reset_to_selection()
            return True
        return False

    def _determine_winner(self):
        for a, b, c in WINNING_LINES:
            if self.game_board[a] == self.game_board[b] == self.game_board[c] != "-":
                return self.game_board[a]
        return None


if __name__ == "__main__":
    root = CTk()
    app = TicTacToeApp(root)
    root.mainloop()
