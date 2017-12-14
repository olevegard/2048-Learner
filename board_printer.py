import math


def get_top_bottom_line(length: int):
    fill_character_count = (8 * length) + (length - 1)
    return "|" + "-" *  fill_character_count + "|"


def get_empty_line(length: int):
    return  "|" + "{:^8}|".format("") * length


def get_line_with_num(numbers):
    line = "|"
    for n in numbers:
        line += "{:^8}|".format(n if n else "")

    return line


def get_grid(grid : list):
    length = int(math.sqrt(len(grid)))
    line = ""
    for i in range(0,length):
        line += get_top_bottom_line(length=length) + "\n"
        line += get_empty_line(length=length) + "\n"
        line += get_line_with_num(numbers=grid[i * length: (i + 1) * length]) + "\n"
        line += get_empty_line(length=length) + "\n"

    line += get_top_bottom_line(length=length) + "\n"

    return line


def print_board(grid : list):
    print(get_grid(grid))


CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
def clear_board():
    for _ in range(18):
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)


def print_score(score):
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print("Score " + str(score))
"""
get_grid(grid=[

    0,   32,
])

get_grid(grid=[
    0,     4,   8,
    16,   0,  64,
    128, 256, 0,
])

get_grid(grid=[
    0,     4,   8, 0,
    16,   0,  64, 0,
    128, 256, 0, 0,
    512, 1024, 0, 4096,
])


print_board([
    0,     4,   8, 0,
    16,   0,  64, 0,
    128, 256, 0, 0,
    512, 1024, 0, 4096,
])

print(str([
    0,     4,   8, 0,
    16,   0,  64, 0,
    128, 256, 0, 0,
    512, 1024, 0, 4096,
][0::4]))

print(str([
    0,     4,   8, 0,
    16,   0,  64, 0,
    128, 256, 0, 0,
    512, 1024, 0, 4096,
][1::4]))

print(str([
    0,     4,   8, 0,
    16,   0,  64, 0,
    128, 256, 0, 0,
    512, 1024, 0, 4096,
][2::4]))

print(str([
    0,     4,   8, 0,
    16,   0,  64, 0,
    128, 256, 0, 0,
    512, 1024, 0, 4096,
][3::4]))
print("\n\n\n\n")
"""
