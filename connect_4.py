import numpy as np

WIN_STATES = [
    # Horizontal
    ([0]*4, range(0, 4)),
    ([0]*4, range(1, 5)),
    ([0]*4, range(2, 6)),
    ([0]*4, range(3, 7)),

    ([1]*4, range(0, 4)),
    ([1]*4, range(1, 5)),
    ([1]*4, range(2, 6)),
    ([1]*4, range(3, 7)),

    ([2]*4, range(0, 4)),
    ([2]*4, range(1, 5)),
    ([2]*4, range(2, 6)),
    ([2]*4, range(3, 7)),

    ([3]*4, range(0, 4)),
    ([3]*4, range(1, 5)),
    ([3]*4, range(2, 6)),
    ([3]*4, range(3, 7)),

    ([4]*4, range(0, 4)),
    ([4]*4, range(1, 5)),
    ([4]*4, range(2, 6)),
    ([4]*4, range(3, 7)),

    ([5]*4, range(0, 4)),
    ([5]*4, range(1, 5)),
    ([5]*4, range(2, 6)),
    ([5]*4, range(3, 7)),

    # Vertical
    (range(0, 4), [0]*4),
    (range(1, 5), [0]*4),
    (range(2, 6), [0]*4),

    (range(0, 4), [1]*4),
    (range(1, 5), [1]*4),
    (range(2, 6), [1]*4),

    (range(0, 4), [2]*4),
    (range(1, 5), [2]*4),
    (range(2, 6), [2]*4),

    (range(0, 4), [3]*4),
    (range(1, 5), [3]*4),
    (range(2, 6), [3]*4),

    (range(0, 4), [4]*4),
    (range(1, 5), [4]*4),
    (range(2, 6), [4]*4),

    (range(0, 4), [5]*4),
    (range(1, 5), [5]*4),
    (range(2, 6), [5]*4),

    (range(0, 4), [6]*4),
    (range(1, 5), [6]*4),
    (range(2, 6), [6]*4),

    # Diag \
    (range(0, 4), range(0, 4)),
    (range(0, 4), range(1, 5)),
    (range(0, 4), range(2, 6)),
    (range(0, 4), range(3, 7)),

    (range(1, 5), range(0, 4)),
    (range(1, 5), range(1, 5)),
    (range(1, 5), range(2, 6)),
    (range(1, 5), range(3, 7)),

    (range(2, 6), range(0, 4)),
    (range(2, 6), range(1, 5)),
    (range(2, 6), range(2, 6)),
    (range(2, 6), range(3, 7)),

    # Diag /
    (range(3, -1, -1), range(1, 5)),
    (range(3, -1, -1), range(0, 4)),
    (range(3, -1, -1), range(2, 6)),
    (range(3, -1, -1), range(3, 7)),

    (range(4, 0, -1), range(0, 4)),
    (range(4, 0, -1), range(1, 5)),
    (range(4, 0, -1), range(2, 6)),
    (range(4, 0, -1), range(3, 7)),

    (range(5, 1, -1), range(0, 4)),
    (range(5, 1, -1), range(1, 5)),
    (range(5, 1, -1), range(2, 6)),
    (range(5, 1, -1), range(3, 7)),
]


class State:
    def __init__(self):
        self.board = np.zeros((2, 6, 7), dtype=bool)
        self.current_player = 0

    def clone(self):
        new_state = State()
        new_state.board = np.array(self.board, copy=True)
        new_state.current_player = self.current_player
        return new_state

    def get_valid_actions(self):
        return ~self.board[:, 0].any(0)

    def take_action(self, i):
        for j in reversed(range(6)):
            if not self.board[0, j, i] and not self.board[1, j, i]:
                self.board[self.current_player, j, i] = True
                break
        self.current_player = 1 if self.current_player == 0 else 0
        return self

    def is_game_over(self):
        return not self.get_valid_actions().any() or self.get_winner() is not None

    def get_score(self):
        winner = self.get_winner()
        if winner == 0:
            return 1
        elif winner is not None:
            return -1
        elif not self.get_valid_actions().any():
            return 0
        else:
            raise Exception('Game not over.')

    def get_winner(self):
        if self.player_won(0):
            return 0
        elif self.player_won(1):
            return 1
        return None

    def player_won(self, player):
        return any([self.board[player][s].all() for s in WIN_STATES])

    def __repr__(self):
        s = ''
        for j in range(6):
            for i in range(7):
                if self.board[0, j, i]:
                    s += '🔴'
                elif self.board[1, j, i]:
                    s += '🔵'
                else:
                    s += '⚪'
            s += '\n'
        return s

    def __eq__(self, other):
        return np.array_equal(self.board, other.board) and self.current_player == other.current_player

    def __hash__(self):
        return hash((self.board.tostring(), self.current_player))

# http://mcts.ai/code/python.html
