from random import choice

from game_functions import evaluate_board_state, get_ordered_moves, has_moves_left


def minimax_search(board_state: list[str], current_depth: int, is_maximizing: bool,
                   alpha: float, beta: float, depth_limit: int) -> int:
    """
        Perform a Minimax search with alpha-beta pruning from the current board state to compute the best
        achievable score for the current player.

            This function explores the game tree from the given board position up to
            a maximum depth and returns an integer score representing the outcome from X's perspective.
            It uses alpha-beta pruning to eliminate branches that cannot improve the outcome
            (based on the current `alpha` and `beta` bounds), which optimizes the search.
            For each possible move, the function temporarily applies that move to `board_state`,
            recursively evaluates the result, and then backtracks (undoes the move).

            Args:
                board_state (list[str]): The current game board as a list of strings
                (e.g., ["X", "-", "O", ...]), where "X" and "O" represent player moves and "-"
                represents an empty cell. This list is modified in-place during the search
                but is restored to its original state after exploring each move.
                current_depth (int): The current depth in the search tree (number of moves
                simulated so far, with 0 for the initial call).
                is_maximizing (bool): True if the current turn is the maximizing player ("X"),
                or False if the current turn is the minimizing player ("O"). When True, the function
                will try to maximize the score; when False, it will try to minimize the score.
                alpha (float): The best score achieved so far by the maximizing player
                (initially set to negative infinity). This is the lower bound for pruning.
                beta (float): The best score achieved so far by the minimizing player
                (initially set to positive infinity). This is the upper bound for pruning.
                depth_limit (int): The maximum depth to explore in the game tree. If `current_depth`
                equals this limit, the search will stop and return the heuristic evaluation of the board
                at that point.

            Returns:
                int: The evaluated score of the board from X's perspective, assuming optimal play
                from both players up to the given depth. Typically, a positive value (e.g., +100)
                indicates a win or favorable outcome for "X", a negative value (e.g., -100) indicates
                a win for "O", and 0 indicates a draw or neutral outcome. A terminal game state
                (win, loss, or draw) or reaching the depth limit will cause the function to return
                the board's static evaluation immediately.
    """
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


def minimax_plain(board_state: list[str], current_depth: int, is_maximizing: bool,
                  depth_limit: int) -> int:
    """
        Perform a Minimax search without alpha-beta pruning from the current board state to compute
        the best achievable score.

            This function explores all possible moves from the current board state up to a given
            depth limit using the basic Minimax algorithm (no pruning). It returns an integer score
            representing the outcome from X's perspective. The search will consider every possible
            move sequence up to the depth limit. For each move, the function modifies `board_state`
            by placing a move, calls itself recursively to evaluate the outcome, and then backtracks
            by removing the move.

            Args:
                board_state (list[str]): The current game board as a list of strings
                (using "X", "O", and "-" to represent player moves and empty cells). This list is
                modified in-place to simulate moves and is restored after exploring each move.
                current_depth (int): The current depth in the recursion (number of moves played
                in the simulated sequence so far).
                is_maximizing (bool): True if the current turn is the maximizing player ("X"),
                or False if it is the minimizing player ("O"). When True, the function will choose
                the move that maximizes the score; when False, it will choose the move that
                minimizes the score.
                depth_limit (int): The maximum depth to search in the game tree. When `current_depth`
                equals this limit, the function returns the static evaluation of the board without
                exploring further moves.

            Returns:
                int: The best possible score from the given board state, from X's perspective.
                A score of +100 typically indicates a win for "X", -100 indicates a win for "O",
                and 0 indicates a draw or a neutral outcome. The evaluation is based on optimal
                play for both players and the function returns immediately if a terminal state is
                reached or the depth limit is met.
    """
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


def choose_move_with_noise(candidates: list[tuple[int, int]], player_symbol: str, difficulty: int) -> int:
    """
        Select one move from the list of scored candidate moves. Lower difficulty levels introduce
        more randomness in the selection.

        Given a list of possible moves and their evaluation scores, this helper function chooses
        one move index to return. For high difficulty levels (5 and above), it deterministically
        selects the move with the optimal score for the given player. For lower difficulty levels
        (below 5), it allows some suboptimal choices: any move with a score close to the best score
        is considered, and one of these near-optimal moves is chosen at random. This simulates
        less-than-perfect play at easier difficulties.

            Args:
                candidates (list[tuple[int, int]]): A list of `(index, score)` pairs for all
                available moves, where `index` is a board position and `score` is the evaluated
                outcome for that move (higher scores favor "X", lower scores favor "O").
                player_symbol (str): The symbol of the player for whom the move is being selected
                ("X" for the maximizer or "O" for the minimizer). This determines whether the best score
                is the maximum or minimum value among the candidates.
                difficulty (int): The difficulty level from 1 (easiest) to 9 (hardest). Lower values
                introduce more randomness in move selection, whereas higher values always pick
                the optimal move. For example, at difficulty 5 or above the highest-score move is
                always chosen, while at difficulty 1 the choice might be any move within a broad
                range of the best score.

            Returns:
                int: The index of the chosen move from the candidates list. This index corresponds
                to a position on the game board that the AI will take as its move.
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


def compute_best_move(board_state: list[str], player_symbol: str, depth_limit: int, difficulty: int) -> int:
    """
        Compute the best move index for the given player using a Minimax search with alpha-beta pruning.

        This function determines the optimal move for `player_symbol` on the current board by
        evaluating all possible moves up to a certain depth. It uses an alpha-beta-pruned
        Minimax search to calculate a score for each potential move, then applies the difficulty
        setting to potentially introduce variability in the final choice. In practice, the function
        simulates every legal move for the player, predicts the outcome assuming optimal play
        (up to `depth_limit` moves ahead), and then selects a move index based on those outcomes
        and the chosen difficulty.

        Args:
            board_state (list[str]): The current board state as a list of strings
            (with "X" for player X, "O" for player O, and "-" for empty spaces).
            player_symbol (str): The symbol of the player whose turn it is ("X" or "O").
            This is the player for whom the best move will be computed.
            depth_limit (int): The maximum search depth for the Minimax algorithm.
            A higher value means looking further ahead in the game (more moves evaluated),
            which can increase accuracy at the cost of more computation.
            difficulty (int): The difficulty level (1-9) that influences move selection.
            Lower difficulties may result in a move that is not strictly optimal
            (to simulate human-like mistakes), while a difficulty of 9 will always choose
            the optimal move. This is achieved by possibly selecting a near-optimal move
            at random when difficulty is below 5.

        Returns:
            int: The index (0-based) of the chosen move on the board for the given player.
            This index indicates where the AI will place its mark. **Note:** This function
            assumes there is at least one empty cell in `board_state` when called
            (i.e., it should not be invoked on a full board).
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


def compute_best_move_plain(board_state: list[str], player_symbol: str, depth_limit: int, difficulty: int) -> int:
    """
        Compute the best move index for the given player using a plain Minimax search
        (no alpha-beta pruning).

        This function is similar to `compute_best_move` but uses the basic Minimax algorithm
        without alpha-beta pruning. It evaluates each possible move for `player_symbol` by
        exploring game outcomes up to the specified depth limit, then chooses a move
        based on those evaluations and the difficulty setting. Because it does not prune
        branches, this approach may be slower for deep searches, but it should reach the
        same conclusions about optimal moves as the pruned version.

        Args:
            board_state (list[str]): The current game board state as a list of strings
            (using "X", "O", and "-" for empty positions).
            player_symbol (str): The symbol of the player whose move is being calculated
            ("X" or "O").
            depth_limit (int): The maximum depth for the Minimax search. When this depth is
            reached, the algorithm stops exploring further moves in that branch.
            difficulty (int): The difficulty level (1-9) controlling the randomness of move s
            election. As with `compute_best_move`, lower difficulty values can cause a near-optimal
            move to be chosen instead of the absolute best move, to simulate imperfect play.

        Returns:
            int: The index of the chosen move (0-based) that the player should make. This value
            corresponds to a position in `board_state` that is currently empty. It is assumed
            that at least one empty cell is available on the board when this function is called.
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