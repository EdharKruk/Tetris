import pytest
from piece import Piece, get_shape
from grid import create_grid, convert_shape_format, valid_space, clear_rows, check_lost

@pytest.fixture
def piece():
    return get_shape()

@pytest.fixture
def grid():
    return create_grid()

def test_piece_initial_position(piece):
    assert piece.x == 5
    assert piece.y == 0

def test_convert_shape_format(piece):
    positions = convert_shape_format(piece)
    assert len(positions) > 0 

def test_valid_space(grid, piece):
    assert valid_space(piece, grid) == True  

def test_invalid_space(grid, piece):
    piece.y = 18  
    piece.x = 0  
    assert valid_space(piece, grid) == False  

def test_clear_rows():
    locked_positions = {(0, 19): (255, 255, 255), (1, 19): (255, 255, 255), (2, 19): (255, 255, 255),
                        (3, 19): (255, 255, 255), (4, 19): (255, 255, 255), (5, 19): (255, 255, 255),
                        (6, 19): (255, 255, 255), (7, 19): (255, 255, 255), (8, 19): (255, 255, 255),
                        (9, 19): (255, 255, 255)}
    grid = create_grid(locked_positions)
    assert clear_rows(grid, locked_positions) == 1  

def test_check_lost():
    locked_positions = {(0, 0): (255, 255, 255)}
    assert check_lost(locked_positions) == True  

def test_piece_rotation(grid, piece):
    piece.rotation = 0
    positions_before = convert_shape_format(piece)
    piece.rotation = 1
    positions_after = convert_shape_format(piece)
    assert positions_before != positions_after  

if __name__ == "__main__":
    pytest.main()
 