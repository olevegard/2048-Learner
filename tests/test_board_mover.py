import board_mover


def test_that_we_can_replace_one_number():
    assert board_mover.set_next_empty_position(0, [0, 0, 0, 2]) == [2, 0, 0, 0]

def test_that_maybe_replace_only_changes_one_number():
    assert board_mover.set_next_empty_position(0, [0, 4, 0, 2]) == [4, 0, 0, 2]

def test_that_maybe_replace_resoects_index():
    assert board_mover.set_next_empty_position(2, [0, 4, 0, 0]) == [0, 4, 0, 0]

def test_that_we_can_move_grid_line_left_with_one_number():
    assert board_mover.move_grid_line_left([0,0,0,2]) == [2,0,0,0]

def test_that_we_can_move_grid_line_left_with_several_numbers():
    assert board_mover.move_grid_line_left([0,0,4,2]) == [4,2,0,0]
    assert board_mover.move_grid_line_left([0,8,4,2]) == [8,4,2,0]

def test_that_we_can_move_grid_line_left_with_all_numbers():
    assert board_mover.move_grid_line_left([16,8,4,2]) == [16,8,4,2]

def test_that_we_can_move_grid_line_left_with_spaces_between_numbers():
    assert board_mover.move_grid_line_left([0,8,0,2]) == [8,2,0,0]

def test_that_join_adjecent_numbers_doesnt_change_grid():
    assert board_mover.join_adjecent_numbers([4,0,0,0]) == [4,0,0,0]
    assert board_mover.join_adjecent_numbers([2,0,4,0]) == [2,0,4,0]

def test_that_join_adjecent_numbers_joins_numbers():
    assert board_mover.join_adjecent_numbers([2,2,0,0]) == [4,0,0,0]
    assert board_mover.join_adjecent_numbers([0,0,4,4]) == [0,0,8,0]

def test_that_join_adjecent_numbers_joins_numbers_with_spaces_between():
    assert board_mover.join_adjecent_numbers([2,0,0,2]) == [4,0,0,0]
    assert board_mover.join_adjecent_numbers([4,0,0,4]) == [8,0,0,0]

def test_that_join_adjecent_numbers_joins_numbers_at_correct_index():
    assert board_mover.join_adjecent_numbers([0,4,4,0]) == [0,8,0,0]
    assert board_mover.join_adjecent_numbers([0,0,8,8]) == [0,0,16,0]

def test_that_join_adjecent_numbers_joins_numbers_at_correct_index_with_multiple_possible_joins():
    assert board_mover.join_adjecent_numbers([2,2,2,0]) == [4,0,2,0]
    assert board_mover.join_adjecent_numbers([0,4,4,4]) == [0,8,0,4]
    assert board_mover.join_adjecent_numbers([8,0,8,8]) == [16,0,0,8]

def test_that_join_multiple_groups():
    assert board_mover.join_adjecent_numbers([2,2,4,4]) == [4,0,8,0]
    assert board_mover.join_adjecent_numbers([4,4,2,2]) == [8,0,4,0]

def test_that_join_multiple_groups_of_same_number():
    assert board_mover.join_adjecent_numbers([2,2,2,2]) == [4,0,4,0]
    assert board_mover.join_adjecent_numbers([4,4,4,4]) == [8,0,8,0]

def test_that_we_cant_join_numbers_with_different_number_between():
    assert board_mover.join_adjecent_numbers([2,4,2,0]) == [2,4,2,0]
    assert board_mover.join_adjecent_numbers([4,8,4,4]) == [4,8,8,0]

def test_that_we_move_left_and_join():
    assert board_mover.move_grid_line_left([0,4,0,0]) == [4,0,0,0]
    assert board_mover.move_grid_line_left([0,2,2,0]) == [4,0,0,0]
    assert board_mover.move_grid_line_left([0,2,2,2]) == [4,2,0,0]
    assert board_mover.move_grid_line_left([2,2,2,2]) == [4,4,0,0]


