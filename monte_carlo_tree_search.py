import connect_4
import numpy as np

c_puct = 1

class Node:
    def __init__(self, p: float, siblings: dict):
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = p
        self.siblings = siblings

    def u(self):
        return c_puct * self.P * np.math.sqrt(sum(sibling.N for sibling in self.siblings.values())) / (1 + self.N)


class MCTS:
    def __init__(self, state: connect_4.State):
        self.state = state
        self.children = {}
        actions = np.flatnonzero(self.state.get_valid_actions())
        prior = 1/len(actions)
        for a in actions:
            self.children[a] = Node(prior, self.children)


