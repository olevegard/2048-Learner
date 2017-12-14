def get_score(board):
    return sum([x ** 2 for x in board if x != 0])