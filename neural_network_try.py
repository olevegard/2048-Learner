import numpy as np

import board_mover
import board_utils
import board_printer


# Board
board = [
    2, 8, # x0, x1
    2, 4] # x2 x3


verbose = False

print("Score before : " + str(board_utils.get_score(board)))

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
        self.weight = 0.5

    def update(self, input_1, input_2):
        if input_1 == input_2:
            self.val = 0
        else:
            self.val = abs(1 / abs((input_1 - input_2)))

        do_print("Inputs : {}, {} Res : {}".format(input_1, input_2, self.val))

    def calculate(self):
        result = self.weight * self.val
        sigm = sigmoid(result) if self.val != 0 else 1
        do_print("Value : {:6.4f} Weighted value : {:6.4f} sigmoid {:6.4f}".format(self.val, result, sigm) )

        return sigm


def get_nodes():
    nodes = []

    for i in range(len(board) - 1):
        j = i + 1
        while j < len(board):
            print("Adding node {}. {}".format(i, j))
            n = Node()
            n.update(board[i], board[j])
            nodes.append(n)
            j += 1

    return nodes

nodes = get_nodes()

left = nodes[0].calculate() + nodes[5].calculate()
down = nodes[1].calculate() + nodes[4].calculate()

print("Left : " + str(left))
print("Down : " + str(down))

print(board_printer.print_board(board))

if left > down:
    board = board_mover.move_all_left(board)
else:
    board = board_mover.move_all_down(board)


print("Score after : " + str(board_utils.get_score(board)))
print(board_printer.print_board(board))


