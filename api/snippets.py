import random

import api.constants as c


def count_hidden_cells(board):
    count = 0
    for row in board:
        for cell in row:
            if cell == c.HIDDEN_CELL:
                count += 1
    return count


def init_array(cols, rows, value):
    return [[value] * cols for i in range(rows)]    # noqa


def insert_mines(board, mines_quantity):
    rows = len(board)
    assert rows > 0
    cols = len(board[0])
    assert cols > 0
    assert mines_quantity < rows * cols
    for i in range(mines_quantity): # noqa
        flag = True
        while flag:
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)
            if board[y][x] != c.MINE_CELL:
                board[y][x] = c.MINE_CELL
                update_adjacent_cells(board, x, y)
                flag = False


def show_adjacent_cells(board, mboard, x, y):
    pivot_list = [-1, 0, 1]
    rows = len(board)
    assert rows == len(mboard)
    cols = len(board[0])
    assert cols == len(mboard[0])
    for dx in pivot_list:
        tx = x + dx
        if tx < 0 or tx >= cols:
            continue
        for dy in pivot_list:
            ty = y + dy
            if ty < 0 or ty >= rows:
                continue
            if mboard[ty][tx] != c.HIDDEN_CELL:
                continue
            if board[ty][tx] == c.MINE_CELL:
                continue
            if board[ty][tx] == c.SAFE_CELL:
                mboard[ty][tx] = c.OPEN_CELL
                show_adjacent_cells(board, mboard, tx, ty)
            else:
                mboard[ty][tx] = str(board[ty][tx])


def update_adjacent_cells(board, x, y):
    pivot_list = [-1, 0, 1]
    rows = len(board)
    assert rows > 0
    cols = len(board[0])
    assert cols > 0
    for dx in pivot_list:
        tx = x + dx
        if tx < 0 or tx >= cols:
            continue
        for dy in pivot_list:
            ty = y + dy
            if ty < 0 or ty >= rows:
                continue
            if board[ty][tx] != c.MINE_CELL:
                board[ty][tx] += 1
