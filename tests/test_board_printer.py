import board_printer

def draw_grid(grid : list):
    length = int(math.sqrt(len(grid)))
    line = ""
    for i in range(0,length):
        line += get_empty_line(length=length) + "\n"
        line += get_line_with_num(numbers=grid[i * length: (i + 1) * length]) + "\n"
        line += get_empty_line(length=length) + "\n"

    line += get_top_bottom_line(length=length) + "\n"

    print(line)


grid=[
    2,     4,   8,
    16,   32,  64,
    128, 256, 512,
]

def test_top_bottom_line():
    assert board_printer.get_top_bottom_line(length=2) == "|-----------------|"
    assert board_printer.get_top_bottom_line(length=3) == "|--------------------------|"
    assert board_printer.get_top_bottom_line(length=4) == "|-----------------------------------|"


def test_empty_line():
    assert board_printer.get_empty_line(length=2) == "|        |        |"
    assert board_printer.get_empty_line(length=3) == "|        |        |        |"
    assert board_printer.get_empty_line(length=4) == "|        |        |        |        |"


def test_get_line_with_num_single_line():
    assert board_printer.get_line_with_num(numbers=[4, 0]) == "|   4    |        |"
    assert board_printer.get_line_with_num(numbers=[2, 0, 8]) == "|   2    |        |   8    |"
    assert board_printer.get_line_with_num(numbers=[0, 2, 4, 8]) == "|        |   2    |   4    |   8    |"


def test_get_board():
    board_string = board_printer.get_grid(grid=[2, 4, 8, 0])

    assert "|-----------------|" in board_string
    assert "|        |        |" in board_string
    assert "|   2    |   4    |" in board_string
    assert "|   8    |        |" in board_string

    assert "|-----------------|\n" \
           "|        |        |\n" \
           "|   2    |   4    |\n" \
           "|        |        |\n" \
           "|-----------------|\n" \
           "|        |        |\n" \
           "|   8    |        |\n" \
           "|        |        |\n" \
           "|-----------------|\n" \
           == board_string

    board_string = board_printer.get_grid(grid=[
        8, 8, 16, 0,
        16, 0, 32, 64,
        32, 128, 16, 4096,
        128, 0, 1024, 8192,
    ])

    assert "|-----------------------------------|" in board_string
    assert "|        |        |        |        |" in board_string
    assert "|   8    |   8    |   16   |        |" in board_string
    assert "|   16   |        |   32   |   64   |" in board_string
    assert "|   32   |  128   |   16   |  4096  |" in board_string
    assert "|  128   |        |  1024  |  8192  |" in board_string

    assert "|-----------------------------------|\n" \
           "|        |        |        |        |\n" \
           "|   8    |   8    |   16   |        |\n" \
           "|        |        |        |        |\n" \
           "|-----------------------------------|\n" \
           "|        |        |        |        |\n" \
           "|   16   |        |   32   |   64   |\n" \
           "|        |        |        |        |\n" \
           "|-----------------------------------|\n" \
           "|        |        |        |        |\n" \
           "|   32   |  128   |   16   |  4096  |\n" \
           "|        |        |        |        |\n" \
           "|-----------------------------------|\n" \
           "|        |        |        |        |\n" \
           "|  128   |        |  1024  |  8192  |\n" \
           "|        |        |        |        |\n" \
           "|-----------------------------------|\n" == board_string
