import math
import random


# TODO: Implement a list that works like the default one, but isn't a reference type and has a revers() function that returns a copy
def reverse(to_reverse):
    new_list = to_reverse.copy()

    new_list.reverse()
    return new_list

def equals(list_1, list_2):
    if len(list_1) != len(list_2):
        return False

    for i in range(len(list_1)):
        if list_1[i] != list_2[i]:
            return False


    return True

def find_index_of_nth(list_, x, n):
    found_count = 0

    for i in range(len(list_)):
        if list_[i] == x:
            if found_count == n:
                return i
            found_count += 1

    raise Exception("Couldn't find {} occurance of {} in {}".format(n, x, list_ ))


def insert_random(grid):
    """
    Inserts a random number ( 2 or 4 ) in a cell that doesn't have a number.


    :param grid: The grid to insert the number in
    :return: The same grid with the number inserter
    """

    # TODO 2 : Improve
    count_empty = grid.count(0)
    index = random.randrange(start=0, stop=count_empty)
    digit_to_enter = random.randrange(start=1, stop=2) * 2
    with_random = grid.copy()

    index = find_index_of_nth(with_random, 0, index)
    with_random[index] = digit_to_enter

    return with_random


# TODO : There is a bug where move_left and move_right switches direction ?

def move_all_left(grid: list):
    return move_all(grid, move_func=move_grid_line_left)

def move_all_right(grid: list):
    return move_all(grid, move_func=move_grid_line_right)

def move_all_down(grid: list):
    return move_all_vertical(grid, move_func=move_grid_line_right)

def move_all_up(grid: list):
    return move_all_vertical(grid, move_func=move_grid_line_left)

def move_all_vertical(grid: list, move_func):
    row_lenght = int(math.sqrt(len(grid)))
    for i in range(0, row_lenght):
        grid[i::row_lenght] = move_func(grid[i::row_lenght])

    return grid

def move_all(grid: list, move_func):
    row_lenght = int(math.sqrt(len(grid)))
    for i in range(0, row_lenght):
        grid[row_lenght * i:(row_lenght  * i ) + row_lenght] = move_func(grid[row_lenght * i:(row_lenght * i ) + row_lenght])

    return grid


def move_grid_line_right(grid: list) -> list:
    # TODO: Find a better way that doesn't involve  so many steps. Ideally a revers() method that returns a new copy
    return reverse(move_grid_line_left(reverse(grid)))


def move_grid_line_left(grid: list) -> list:
    """
    Base method used to move a single row to the left
    I.e.
        [0,0,0,2]) == [2,0,0,0]
        [0,0,4,2]) == [4,2,0,0]
        [0,8,4,2]) == [8,4,2,0]
        [16,8,4,2]) == [16,8,4,2]
        [0,8,0,2]) == [8,2,0,0]

    This method is also used for moving right/up/down in addition to left,
    thien it flips the array for moving right to left, and use slice [row::row_length] to find the columns


    :param grid: The grid to move. Should be a single row, not the entire board
    :return: The new line, with all digits moved to the left
    """
    new_grid = join_adjacent_numbers(grid.copy())

    for i in range(0, len(new_grid)):
        if not new_grid[i]:
            new_grid = set_next_empty_position(i, new_grid)

    return new_grid


def set_next_empty_position(index_to_replace, grid):
    """

    :param index_to_replace: The index to replace ( the index of the next column that has the value 0 )
    :param grid: The current row
    :return: The row with the desired index set
    """
    new_grid = grid.copy()

    for j in range(index_to_replace, len(new_grid)):
        if new_grid[j]:
            if new_grid[index_to_replace] == new_grid[j]:
                new_grid[index_to_replace] = new_grid[j] * 2
            else:
                new_grid[index_to_replace] = new_grid[j]
            new_grid[j] = 0
            break

    return new_grid


def join_adjacent_numbers(grid):
    """
    Joins/merges two adjecent numbers ( or with spaces between )
    Will always be join at the index of the first number
    Will only join each number once

    Eg. :
        [ 2 2 ] = [ 4 0 ]
        [ 2 0 2 ] = [ 4 0 0 ]
        [ 0 2 2 ] = [ 0 4 0 ]
        [ 4 4 2 2 ] = [ 8 0 4 0 ]
        [ 2 2 2 2 ] = [ 4 0 4 0 ]


    :param grid: The grid line with the numbers to join
    :return: The grid with all numbers joined
    """
    new_grid = grid.copy()

    for i in range(0, len(new_grid) - 1):
        if not new_grid[i]:
            continue

        for j in range(i + 1, len(new_grid)):
            if new_grid[j] == 0:
                continue
            if new_grid[i] == new_grid[j]:
                new_grid[i] *= 2
                new_grid[j] = 0
            break

    return new_grid
