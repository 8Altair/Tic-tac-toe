from random import choice

from game_functions import evaluate_board_state, get_ordered_moves, has_moves_left


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


def choose_move_with_noise(candidates, player_symbol, difficulty):
    """
        candidates : list[(index, score)]
        difficulty : 1-9
        Returns an index.  For difficulty < 5 we allow moves that are
        *close* to the best score and pick randomly among them.
    """
    tolerance = max(0, (5 - difficulty) * 5)
    if player_symbol == "X":
        best = max(score for _, score in candidates)
        # X is a maximizer → keep moves not much worse than best
        pool = [i for i, score in candidates if best - score <= tolerance]
    else:
        best = min(score for _, score in candidates)
        pool = [i for i, score in candidates if score - best <= tolerance]

    # Easy / medium → random among pool
    if difficulty < 5 and len(pool) > 1:
        return choice(pool)

    # Hard → deterministic best
    return pool[0]


def compute_best_move(board_state, player_symbol, depth_limit, difficulty):
    """
        Alpha-beta version.
        Returns the chosen move index.
    """
    candidates = []
    alpha = float("-inf")
    beta  = float("inf")

    for i in range(len(board_state)):
        if board_state[i] != "-":
            continue
        board_state[i] = player_symbol
        next_is_max = (player_symbol == "O")    # human turn next if AI just played
        value = minimax_search(board_state, 0, next_is_max, alpha, beta, depth_limit)
        board_state[i] = "-"
        candidates.append((i, value))

    return choose_move_with_noise(candidates, player_symbol, difficulty)


def compute_best_move_plain(board_state, player_symbol, depth_limit, difficulty):
    """
        Plain minimax (no pruning).
    """
    candidates = []
    for i in range(len(board_state)):
        if board_state[i] != "-":
            continue
        board_state[i] = player_symbol
        next_is_max = (player_symbol == "O")
        value = minimax_plain(board_state, 0, next_is_max, depth_limit)
        board_state[i] = "-"
        candidates.append((i, value))

    return choose_move_with_noise(candidates, player_symbol, difficulty)