def move_grid_line_left(grid: list) -> list:
    """
    Base method used to move a single row to the left
    I.e.
        [0,0,0,2]) == [2,0,0,0]
        [0,0,4,2]) == [4,2,0,0]
        [0,8,4,2]) == [8,4,2,0]
        [16,8,4,2]) == [16,8,4,2]
        [0,8,0,2]) == [8,2,0,0]

    This method should also be used for moving right/up/down in addition to left,
    just flip the array for moving rightto left, and use slice [row::row_length] to find the columns

    :param grid: The grid to move. Should be a signle row, not the entire board
    :return: The new line, with all digits moved to the left
    """
    new_grid = join_adjecent_numbers(grid.copy())

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


def join_adjecent_numbers(grid):
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
