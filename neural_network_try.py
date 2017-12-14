import numpy as np

import board_mover
import board_utils
import board_printer




verbose = False


def do_print(str):
    if verbose:
        print(str)

# sigmoid function
def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)

    return 1/(1+np.exp(-x))

class Node:
    def __init__(self):
        self.weight = 0.5 * get_random()

    def update(self, input_1, input_2):
        if input_1 == input_2:
            self.val = 0
        else:
            self.val = abs(1 / abs((input_1 - input_2)))

        # do_print("Inputs : {}, {} Res : {}".format(input_1, input_2, self.val))

    def calculate(self):
        result = self.weight * self.val
        sigm = sigmoid(result) if self.val != 0 else 1
        # do_print("Value : {:6.4f} Weighted value : {:6.4f} sigmoid {:6.4f}".format(self.val, result, sigm) )

        return sigm


def get_nodes(board):
    nodes = []

    for i in range(len(board) - 1):
        j = i + 1
        while j < len(board):
            do_print("Adding node {}. {}".format(i, j))

            n = Node()
            n.update(board[i], board[j])

            nodes.append(n)
            j += 1

    return nodes

np.random.seed(0)

def get_random():
    return sigmoid(np.random.random(1)[0], deriv=False) + 0.4

def adjust_weights(nodes, increase):
    for node in nodes:
        if increase:
            node.weight *= max(get_random(), 1.0)
        else:
            node.weight *= min(get_random(), 1.0)


def evaulate_nodes(nodes_left, nodes_down, board):
    left = sum([node.calculate() for node in nodes_left])
    down = sum([node.calculate() for node in nodes_down])

    do_print("Sum left : " + str(left))
    do_print("Sum down : " + str(down))

    if left > down:
        do_print("Move down")
        board = board_mover.move_all_left(board)
    elif left < down:
        do_print("Move up")
        board = board_mover.move_all_down(board)
    else:
        do_print("No change!")

    return board


def print_board_and_score(board):
    board_printer.print_board(board)
    print("Score : " + str(board_utils.get_score(board)))

def train(board, left_should_win = False, down_should_win = False):
    if not left_should_win and not down_should_win:
        print("Either left_win or down_win should be True")
        return
    board = board.copy()

    score_before = board_utils.get_score(board)

    nodes_left = get_nodes(board)
    nodes_down = get_nodes(board)

    print(" Before ".center(80, "="))
    print_board_and_score(board)
    board = evaulate_nodes(nodes_left, nodes_down, board)

    print(" After ".center(80, "="))
    score_after = board_utils.get_score(board)
    print_board_and_score(board)


    if score_after == score_before:
        print(" Score is the same ".center(80, "="))
        if left_should_win:
            adjust_weights(nodes_left, True)
            adjust_weights(nodes_down, False)
        elif down_should_win:
            adjust_weights(nodes_left, True)
            adjust_weights(nodes_down, False)
        print("=" * 80)
        return False
    else:
        print(" Score is higher ".center(80, "="))
        return True

board = [
    2, 8, 2, # x0, x1
    4, 8, 4, # x0, x1
    2, 4, 2] # x2 x3

train(board, left_should_win=False, down_should_win=True)
train(board, left_should_win=False, down_should_win=True)
