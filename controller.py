import board_printer
import board_mover
import getch


# TODO: Don't use global variables



class BoardState:
    def __init__(self, current_board, board_history):
        self.board = [
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            2, 2, 0, 0,
        ]

        board_history = [board.copy()]





board  = None
prev  = None

board = [
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    2, 2, 0, 0,
]

print(" 2048 ".center(80, "=") + "\n")
board_history = [board.copy()]
prev = board.copy()
board_printer.print_score(board)
board_printer.print_board(board)

char = ''
while char != 'q':
    char = getch.getch()

    # Undo
    # ========================================

    # Left
    # ========================================
    if char == 'a':
        board = board_mover.move_all_left(board)

        if not board_mover.equals(prev, board):
            board = board_mover.insert_random(board)

    # Right
    # ========================================
    elif char == 'd':
        board = board_mover.move_all_right(board)

        if not board_mover.equals(prev, board):
            board = board_mover.insert_random(board)

    # Up
    # ========================================
    elif char == 'w':
        board = board_mover.move_all_up(board)

        if not board_mover.equals(prev, board):
            board = board_mover.insert_random(board)

        board_history.append(board.copy())

    # Down
    # ========================================
    elif char == 's':
        board = board_mover.move_all_down(board)

        if not board_mover.equals(prev, board):
            board = board_mover.insert_random(board)

    elif char == 'r':
        board = [
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            2, 2, 0, 0,
        ]

    if char == 'e':
        if len(board_history) > 1:
            board = board_history[-2].copy()
            board_history = board_history[:-1]
    else:
        board_history.append(board.copy())

    board_printer.clear_board()
    board_printer.print_score(board)
    board_printer.print_board(board)


    prev = board.copy()
