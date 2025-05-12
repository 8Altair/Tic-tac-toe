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
BONUS_SCALE = 1.0   # Will be reset each game


def has_moves_left(board_state):
    return "-" in board_state


def evaluate_board_state(board_state):
    for a, b, c in WINNING_LINES:   # Terminal win/loss first
        symbol = board_state[a]
        if symbol == board_state[b] == board_state[c] and symbol != "-":
            return 100 if symbol == "X" else -100

    open_lines_max = open_lines_min = 0
    two_in_row_max = two_in_row_min = 0

    for a, b, c in WINNING_LINES:
        line = (board_state[a], board_state[b], board_state[c])
        if "O" not in line:  # Still winnable for X
            open_lines_max += 1
            if line.count("X") == 2:
                two_in_row_max += 1
        if "X" not in line:  # Still winnable for O
            open_lines_min += 1
            if line.count("O") == 2:
                two_in_row_min += 1

    line_term = BONUS_SCALE * (open_lines_max - open_lines_min)
    threat_term = BONUS_SCALE ** 2 * BONUS * (two_in_row_max - two_in_row_min)

    centre_term = 0
    if board_state[4] == "X":
        centre_term = BONUS_SCALE ** 2 * BONUS
    elif board_state[4] == "O":
        centre_term = -BONUS_SCALE ** 2 * BONUS

    return line_term + threat_term + centre_term

def get_ordered_moves(board_state, player):
    candidates = []
    for i in range(len(board_state)):
        if board_state[i] == "-":
            board_state[i] = player
            score = evaluate_board_state(board_state)
            board_state[i] = "-"
            candidates.append((i, score))

    return [i for i, _ in sorted(candidates, key=lambda pair: pair[1], reverse=(player == "X"))]    # For X (maximizer), sort descending; for O (minimizer), ascending
