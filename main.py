import os, sys

import tkinter as tk
import customtkinter as ctk

from tkinter import messagebox
from customtkinter import CTk, CTkFrame, CTkButton, CTkRadioButton, CTkLabel, CTkOptionMenu

from algorithm_functions import compute_best_move, compute_best_move_plain, has_moves_left
from game_functions import WINNING_LINES, BONUS_SCALE


# Initialize dark theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

DIFFICULTY_OPTIONS = tuple(range(1, 10))
SCALE = BONUS_SCALE

ICON_FILENAME = r"red-x-sign-symbol-icon-letter-x-sign-no-sign-design-transparent-background-free-png"

def resource_path(*parts: str) -> str:
    """
        Return absolute path for dev and PyInstaller onefile.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    base = os.fsdecode(base)
    return os.path.join(base, *parts)

def set_app_icon(win: tk.Tk) -> None:
    # Best option in a packaged EXE: use the EXE's own icon (set via PyInstaller --icon)
    if getattr(sys, "frozen", False):  # Running as a PyInstaller bundle
        try:
            win.iconbitmap(sys.executable)
            return
        except tk.TclError:
            pass  # fall through

    # Otherwise (or if the above failed), use the .ico from the Icon folder
    icon_path = resource_path("Icon", f"{ICON_FILENAME}.ico")
    try:
        win.iconbitmap(icon_path)
        return
    except tk.TclError:
        pass

class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.geometry("700x750")
        self.master.resizable(True, True)

        set_app_icon(self.master)

        self.human_symbol = None
        self.ai_symbol = None
        self.current_turn = None
        self.symbol_choice = tk.StringVar(value="X")
        self.algorithm_variable = tk.StringVar(value="Minimax")
        self.max_search_depth = DIFFICULTY_OPTIONS[0]
        self.difficulty_variable = tk.StringVar(value=str(self.max_search_depth))
        self._setup_selection_panel()

    def _setup_selection_panel(self):
        self.selection_frame = CTkFrame(self.master, width=700, height=750)
        self.selection_frame.pack(expand=True)

        prompt_label = CTkLabel(self.selection_frame, text="Choose your symbol:", font=("Arial", 40, "bold"))
        prompt_label.pack(pady=20, padx=30)

        radio_x = CTkRadioButton(self.selection_frame, text="Play as X", variable=self.symbol_choice,
                                 value="X", font=("Arial", 25), width=150)
        radio_x.pack(pady=5, padx=30, anchor="w")

        radio_o = CTkRadioButton(self.selection_frame, text="Play as O", variable=self.symbol_choice, value="O",
                                 font=("Arial", 25), width=150)
        radio_o.pack(pady=5, padx=30, anchor="w")

        # Algorithm selector
        algorithm_label = CTkLabel(self.selection_frame, text="Algorithm:", font=("Arial", 30))
        algorithm_label.pack(pady=15, padx=30, anchor="w")

        algorithm_menu = CTkOptionMenu(self.selection_frame, variable=self.algorithm_variable,
                                       values=("Minimax", "Alpha-Beta"), width=500, height=45,
                                       font=("Arial", 20), dropdown_font=("Arial", 20))
        algorithm_menu.pack(pady=5, padx=30, anchor="w")

        # Difficulty selector
        difficulty_label = CTkLabel(self.selection_frame, text="Difficulty:", font=("Arial", 30))
        difficulty_label.pack(pady=15, padx=30, anchor="w")

        difficulty_menu = CTkOptionMenu(self.selection_frame, variable=self.difficulty_variable,
                                        values=[str(option) for option in DIFFICULTY_OPTIONS], width=200, height=40,
                                       font=("Arial", 20), dropdown_font=("Arial", 20))
        difficulty_menu.pack(pady=5, padx=30, anchor="w")

        start_button = CTkButton(self.selection_frame, text="Start Game", font=("Arial", 30, "bold"), width=200, height=50,
                                 command=self._start_game)
        start_button.pack(pady=20, padx=30)

    def _start_game(self):
        self.max_search_depth = int(self.difficulty_variable.get())
        global SCALE
        SCALE = self.max_search_depth / 9
        self.human_symbol = self.symbol_choice.get()
        self.ai_symbol = "O" if self.human_symbol == "X" else "X"
        self.current_turn = "X"
        self.selection_frame.destroy()
        self._setup_game_panel()

        if self.current_turn == self.ai_symbol:
            self.master.after(100, self._execute_ai_move)

    def _setup_game_panel(self):
        self.control_frame = CTkFrame(self.master)  # dark‐mode frame
        self.control_frame.pack(pady=10)

        restart_button = CTkButton(self.control_frame, text="Restart", font=("Arial", 30),
                                   command=self._reset_to_selection)
        restart_button.pack(side="left", padx=10)

        self.board_frame = CTkFrame(self.master)
        self.board_frame.pack(expand=True)

        self.cell_buttons = []
        self.game_board = ["-" for _ in range(9)]

        for index in range(9):
            button = CTkButton(self.board_frame, text="", width=150, height=150, font=("Arial", 120),
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
        depth = self.max_search_depth - 1  # Level 1 ⇒ depth 0 search
        if depth < 0:
            depth = 0  # Safety change

        if self.algorithm_variable.get() == "Minimax":
            best_index = compute_best_move_plain(self.game_board, self.current_turn, depth, self.max_search_depth)
        else:
            best_index = compute_best_move(self.game_board, self.current_turn, depth, self.max_search_depth)

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
