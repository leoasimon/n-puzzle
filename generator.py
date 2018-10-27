#! /usr/bin/env python3

from collections import deque
from printer import print_grid 


def fill_top(grid, n, sx, sy, sv):
    for i in range(sx, sx + n):
        grid[sy][i] = sv
        sv += 1
    return grid

def make_goal(size):
    max_val = (size * size) - 1
    grid = [[0 for i in range(size)] for x in range(size)]
    
    print_grid(grid)

if __name__ == "__main__":
    make_goal(3)

