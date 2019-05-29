import numpy as np


class State:
    def __init__(self):
        self.board = np.zeros((2, 6, 7), dtype=bool)
        self.current_player = 0

    def get_valid_actions(self):
        valid_actions = np.ones((7,), dtype=bool)
        for i in range(7):
            if self.board[0, 0, i] or self.board[1, 0, i]:
                valid_actions[i] = False
        return valid_actions

    def take_action(self, i):
        for j in reversed(range(6)):
            if not self.board[0, j, i] and not self.board[1, j, i]:
                self.board[self.current_player, j, i] = True
                break
        self.current_player = 1 if self.current_player == 0 else 0

    def is_game_over(self):
        return not self.get_valid_actions().any()

    def __repr__(self):
        s = ''
        for j in range(6):
            for i in range(7):
                if self.board[0, j, i]:
                    s += '🔴'
                elif self.board[1, j, i]:
                    s += '🔵'
                else:
                    s += '⚫'
            s += '\n'
        return s
