import tkinter as tk
from tkinter import messagebox

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


def has_moves_left(board_state):
    return "-" in board_state


def evaluate_board_state(board_state):
    for a, b, c in WINNING_LINES:
        symbol = board_state[a]
        if symbol == board_state[b] == board_state[c] and symbol != "-":
            return 10 if symbol == "X" else -10
    return 0


def minimax_search(board_state, current_depth, is_maximizing, alpha, beta, depth_limit):
    score = evaluate_board_state(board_state)
    if score == 10 or score == -10 or current_depth == depth_limit or not has_moves_left(board_state):
        return score
    if is_maximizing:
        best_score = float("-inf")
        for index in range(len(board_state)):
            if board_state[index] == "-":
                board_state[index] = "X"
                value = minimax_search(board_state, current_depth + 1, False, alpha, beta, depth_limit)
                board_state[index] = "-"
                best_score = max(best_score, value)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float("inf")
        for index in range(len(board_state)):
            if board_state[index] == "-":
                board_state[index] = "O"
                value = minimax_search(board_state, current_depth + 1, True, alpha, beta, depth_limit)
                board_state[index] = "-"
                best_score = min(best_score, value)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score


def compute_best_move(board_state, player_symbol, depth_limit):
    best_move = -1
    if player_symbol == "X":
        best_value = float("-inf")
    else:
        best_value = float("inf")
    alpha = float("-inf")
    beta = float("inf")
    for index in range(len(board_state)):
        if board_state[index] == "-":
            board_state[index] = player_symbol
            next_is_maximizing = player_symbol == "O"
            move_value = minimax_search(board_state, 0, next_is_maximizing, alpha, beta, depth_limit)
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
        self.selection_frame = tk.Frame(self.master)
        self.selection_frame.pack(expand=True)

        prompt_label = tk.Label(self.selection_frame, text="Choose your symbol:", font=("Arial", 24))
        prompt_label.pack(pady=20)

        self.symbol_choice_var = tk.StringVar(value="X")

        radio_x = tk.Radiobutton( self.selection_frame, text="Play as X", variable=self.symbol_choice_var, value="X", font=("Arial", 18), width=15)
        radio_x.pack(pady=5, anchor="w")

        radio_o = tk.Radiobutton( self.selection_frame, text="Play as O", variable=self.symbol_choice_var, value="O", font=("Arial", 18), width=15)
        radio_o.pack(pady=5, anchor="w")

        start_button = tk.Button(self.selection_frame, text="Start Game", font=("Arial", 24), command=self._start_game,)
        start_button.pack(pady=20)

    def _start_game(self):
        self.human_symbol = self.symbol_choice_var.get()
        self.ai_symbol = "O" if self.human_symbol == "X" else "X"
        self.current_turn = "X"
        self.selection_frame.destroy()
        self._setup_game_panel()
        if self.current_turn == self.ai_symbol:
            self.master.after(100, self._execute_ai_move)

    def _setup_game_panel(self):
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(pady=10)

        restart_button = tk.Button(self.control_frame, text="Restart", font=("Arial", 18), command=self._reset_to_selection,)
        restart_button.pack(side="left", padx=10)

        difficulty_label = tk.Label(self.control_frame, text="Difficulty:", font=("Arial", 18) )
        difficulty_label.pack(side="left")

        self.difficulty_variable = tk.StringVar(value=str(self.max_search_depth))
        difficulty_menu = tk.OptionMenu(self.control_frame, self.difficulty_variable,
                                        *DIFFICULTY_OPTIONS, command=self._on_difficulty_changed, )
        difficulty_menu.config(font=("Arial", 14))
        difficulty_menu.pack(side="left", padx=10)

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(expand=True)

        self.cell_buttons = []
        self.game_board = ["-" for _ in range(9)]

        for index in range(9):
            button = tk.Button( self.board_frame, text="", width=4, height=2, font=("Arial", 48),
                                command=lambda idx=index: self._on_cell_clicked(idx),)
            button.grid(row=index // 3, column=index % 3, padx=5, pady=5)
            self.cell_buttons.append(button)

        self._update_board_ui()

    def _on_difficulty_changed(self, _):
        self.max_search_depth = self.difficulty_variable.get()

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
        best_index = compute_best_move(self.game_board, self.current_turn, self.max_search_depth)
        if best_index != -1:
            self.game_board[best_index] = self.current_turn
            self._update_board_ui()
            if self._check_for_end():
                return
            self.current_turn = self.human_symbol

    def _update_board_ui(self):
        for idx, button in enumerate(self.cell_buttons):
            symbol = self.game_board[idx]
            if symbol == "-":
                button.config(text="", state="normal")
            else:
                button.config(text=symbol, state="disabled")

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
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
