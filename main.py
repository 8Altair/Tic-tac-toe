import tkinter as tk
from tkinter import messagebox

# Set up the game board as a list
board = ["-" for _ in range(9)]
user = None
current_player = None
difficulty_levels = (1, 2, 3, 4, 5, 6)
selected_difficulty = 1


# Define the GUI layout and widgets
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.board_frame, text="", width=6, height=3,
                               command=lambda idx=i: self.handle_click(idx))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        self.replay_button = tk.Button(self.root, text="Replay", command=self.init_game)
        self.replay_button.pack()

        self.difficulty_label = tk.Label(self.root, text="Select difficulty:")
        self.difficulty_label.pack()

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("1")
        self.difficulty_menu = tk.OptionMenu(self.root, self.difficulty_var,
                                             *difficulty_levels, command=self.update_difficulty)
        self.difficulty_menu.pack()

        self.init_game()

    def update_difficulty(self, event=None):
        global selected_difficulty
        selected_difficulty = int(self.difficulty_var.get())

    def init_game(self):
        global user, current_player, board
        user = None
        current_player = None
        board = ["-" for _ in range(9)]

        user_choice = tk.messagebox.askquestion("Choose X or O", "Do you want to play as X?")
        user = 'X' if user_choice == 'yes' else 'O'
        current_player = 'X' if user == 'O' else 'O'
        if current_player == 'X':
            self.ai_move()

        self.update_board_ui()

    def update_board_ui(self):
        for i in range(9):
            if board[i] != "-":
                self.buttons[i].config(text=board[i], state=tk.DISABLED)
            else:
                self.buttons[i].config(text="", state=tk.NORMAL)

    def handle_click(self, idx):
        global current_player
        if 0 <= idx < len(board) and current_player == user and board[idx] == "-":
            board[idx] = user
            self.update_board_ui()
            self.check_game_over()
            current_player = 'O' if current_player == 'X' else 'X'
            if current_player != user:
                self.ai_move()

    def check_game_over(self):
        global board
        for a, b, c in ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)):
            if board[a] == board[b] == board[c] != "-":
                messagebox.showinfo("Game Over", f"{board[a]} wins!")
                self.init_game()
                return
        if "-" not in board:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.init_game()

    def ai_move(self):
        global current_player
        best_move = find_best_move(board, current_player)
        board[best_move] = current_player
        self.update_board_ui()
        self.check_game_over()
        current_player = 'O' if current_player == 'X' else 'X'


def are_moves_left(board):
    return '-' in board


def evaluate(board):
    # Checking for rows for X or O victory
    for row in range(0, 9, 3):
        if board[row] == board[row + 1] == board[row + 2] != '-':
            return 10 if board[row] == 'X' else -10
    # Checking for columns for X or O victory
    for col in range(3):
        if board[col] == board[col + 3] == board[col + 6] != '-':
            return 10 if board[col] == 'X' else -10
    # Checking for diagonals for X or O victory
    if board[0] == board[4] == board[8] != '-':
        return 10 if board[0] == 'X' else -10
    if board[2] == board[4] == board[6] != '-':
        return 10 if board[2] == 'X' else -10
    # Else if none of them have won, then return 0
    return 0


# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, is_max, alpha, beta, max_depth):
    """
        Minimax algorithm with alpha-beta pruning for Tic Tac Toe.

        Args:
            board (list): The current state of the game board.
            depth (int): The current depth in the game tree.
            is_max (bool): Indicates whether it's the maximizing player's turn.
            alpha (float): The best value that the maximizing player currently can guarantee.
            beta (float): The best value that the minimizing player currently can guarantee.
            max_depth (int): The maximum depth to explore in the game tree.

        Returns:
            float: The evaluation value of the current board state.
    """
    # Base case: if the maximum depth is reached or there are no moves left
    if depth == max_depth or not are_moves_left(board):
        return evaluate(board)

    if is_max:
        best = -1000
        for i in range(9):
            if board[i] == '-':
                board[i] = 'X'
                # Recur for the next depth with a minimizing turn
                value = minimax(board, depth + 1, not is_max, alpha, beta, max_depth)
                board[i] = '-'  # Backtrack
                best = max(best, value)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = 1000
        for i in range(9):
            if board[i] == '-':
                board[i] = 'O'
                # Recur for the next depth with a maximizing turn
                value = minimax(board, depth + 1, not is_max, alpha, beta, max_depth)
                board[i] = '-'  # Backtrack
                best = min(best, value)
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best


def find_best_move(board, player):
    """
        Finds the best move for the specified player using the minimax algorithm.

        Args:
            board (list): The current state of the game board.
            player (str): The player for whom the best move is being calculated ('X' or 'O').

        Returns:
            int: The index of the best move for the specified player.
    """
    best_value = float('-inf') if player == 'X' else float('inf')
    best_move = -1
    alpha = float('-inf')
    beta = float('inf')
    max_depth = selected_difficulty
    for i in range(9):
        if board[i] == '-':
            board[i] = player
            # Call minimax to evaluate the current move
            move_value = minimax(board, 0, player == 'O', alpha, beta, max_depth)
            board[i] = '-'  # Backtrack
            # Update the best move if a better move is found
            if (player == 'X' and move_value > best_value) or (player == 'O' and move_value < best_value):
                best_move = i
                best_value = move_value
    return best_move


if __name__ == '__main__':
    # Initialize Tkinter
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
