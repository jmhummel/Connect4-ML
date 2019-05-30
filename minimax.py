import numpy as np
import sys
from timeit import default_timer as timer
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import style

import connect_4

INT_MAX = 1
INT_MIN = -1


class Node:
    def __init__(self, state: connect_4.State, maximizing_player: bool, depth=0):
        self.state = state
        self.maximizing_player = maximizing_player
        self.depth = depth
        self.children = None

    def value(self):
        if self.depth == 0 or self.state.is_game_over():
            # return self.state.get_score()
            value = self.state.get_score()
            print(self.value(), self.state, self.maximizing_player, self.depth)
            return value
        if self.maximizing_player:
            value = INT_MIN
            for child in self.get_children():
                value = max(value, child.value())
            return value
        else:
            value = INT_MAX
            for child in self.get_children():
                value = min(value, child.value())
            return value

    def get_children(self):
        children = []
        for i in np.flatnonzero(self.state.get_valid_actions()):
            child_state = self.state.clone().take_action(i)
            child_node = Node(child_state, not self.maximizing_player, self.depth + 1)
            children.append(child_node)
        return children

    def __hash__(self):
        return hash((self.state, self.maximizing_player))

    def __eq__(self, other):
        return self.state == other.state and self.maximizing_player == other.maximizing_player


# xs = []
# ys = []
# style.use('fivethirtyeight')
# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)


# def animate(i):
#     ax1.clear()
#     ax1.plot(xs, ys)


def minimax(root):
    seen = {}
    stack = [root]

    i = 0
    start = timer()
    min_depth = sys.maxsize
    while stack:
        # xs.append(timer() - start)
        # ys.append(len(stack))
        # ax1.plot(xs, ys)
        # plt.draw()
        # plt.pause(0.001)
        if timer() - start > i:
            # print(len(stack), len(seen), end='\r', flush=True)
            # print(f'\r{i//3600:02}h {(i//60)%60:02}m {i%60:02}s Stack: {len(stack):<6} Seen: {len(seen):<9}', end='', flush=True)
            print(f'{i//3600:02}h {(i//60)%60:02}m {i%60:02}s    Stack: {len(stack):<6} Seen: {len(seen):<9} Min Depth: {min_depth:<6}')
            i += 1
        node = stack.pop()
        if node in seen:
            pass
        elif node.state.is_game_over():
            min_depth = min(min_depth, node.depth)
            seen[node] = node.state.get_score()
            # print(node.state, len(seen), seen[node], node.maximizing_player)
        else:
            if node.children is None:
                node.children = node.get_children()
            unseen = []
            if node.maximizing_player:
                value = INT_MIN
                for child in node.children:
                    if child not in seen:
                        unseen.append(child)
                    else:
                        value = max(value, seen[child])
                    if value == INT_MAX:
                        break
                if unseen and value != INT_MAX:
                    stack.append(node)
                    stack.append(unseen[0])
                else:
                    min_depth = min(min_depth, node.depth)
                    seen[node] = value
                    # print(node.state, len(seen), seen[node], node.maximizing_player)
            else:
                value = INT_MAX
                for child in node.children:
                    if child not in seen:
                        unseen.append(child)
                    else:
                        value = min(value, seen[child])
                    if value == INT_MIN:
                        break
                if unseen and value != INT_MIN:
                    stack.append(node)
                    stack.append(unseen[0])
                else:
                    min_depth = min(min_depth, node.depth)
                    seen[node] = value
                    # print(node.state, len(seen), seen[node], node.maximizing_player)
    return seen[root]


if __name__ == '__main__':
    # ani = animation.FuncAnimation(fig, animate, interval=1000)
    # plt.ion()
    # plt.show()
    print(minimax(Node(connect_4.State(), True)))
