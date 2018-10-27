#! /usr/bin/env python3

from collections import deque
from printer import print_grid 
import sys

def make_loop(grid, size):
    i = 1 # current value for grid
    j = size # current length of side to fill
    max_val = (size * size) - 1 # spiral should stop when i == this
    sx = 0 # starting x position
    sy = 0 # starting y position

    sides = ['top', 'right', 'bottom', 'left']
    side_n = 0
    while (i <= max_val and j >= 1):
        if (side_n == 0):
            # make top
            for k in range(sx, sx + j):
                grid[sy][k] = i
                i += 1
            side_n = (side_n + 1) % len(sides)
            sx += j - 1
            sy += 1
            j -= 1
        elif side_n == 1:
            # make right
            for k in range(sy, sy + j):
                grid[k][sx] = i
                i += 1
            side_n = (side_n + 1) % len(sides)
            sx -= 1
            sy += j - 1
        elif side_n == 2:
            # make bottom
            for k in range(sx, sx - j, - 1):
                grid[sy][k] = i
                i += 1
            side_n = (side_n + 1) % len(sides)
            sx -= j - 1
            sy -= 1
            j -= 1
        else: # side_n == 3
            # make left
            for k in range(sy, sy - j, - 1):
                grid[k][sx] = i
                i += 1
            side_n = (side_n + 1) % len(sides)
            sx += 1
            sy -= j - 1
    return grid

def make_goal(size):
    grid = [[0 for i in range(size)] for x in range(size)]
    grid = make_loop(grid, size)
    grid = tuple(tuple(x) for x in grid)
    return grid
