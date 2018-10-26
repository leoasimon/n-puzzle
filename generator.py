#! /usr/bin/env python3

from collections import deque
from printer import print_grid

def fill_column(grid, rowstart, col, vals):
    i = rowstart
    while vals:
        grid[i][col] = vals.pop(0)
        i += 1

def fill_row(grid, colstart, row, vals):
    i = colstart
    while vals:
        grid[row][i] = vals.pop(0)
        i += 1
    return grid

#top = 0, right = 1, bottom = 2, left = 3
def get_vals(grid, side, size, length, max_val, curr_max, start_val, curr_pos):
    if (curr_max >= max_val):
        return grid
    if (side == 0):
        fill_row(grid, curr_pos[0], curr_pos[1], [x for x in range(start_val, start_val + length)])

    print_grid(grid)
        # get_vals(grid, 1, size, length - 1, max_val, )
    # if (side == 1)
    #     fill_column(grid, curr_pos[1], curr_pos[0], )
    
    
        

def make_goal(size):
    max_val = (size * size) - 1
    line = list(tuple(0 for i in range(size)))
    grid = list(tuple(line for _ in range(size)))
    get_vals(grid, 0, size, size, max_val, size, 1, (0, 0))
    # print_grid(grid)

if __name__ == "__main__":
    make_goal(3)

