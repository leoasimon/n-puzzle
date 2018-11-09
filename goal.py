#! /usr/bin/env python3

import sys
import numpy as np

def _get_sides(grid, n, maxval, v=1, x=0, y=0):
	if v > maxval:
		return grid

	for _ in range(4):
		if v <= maxval:
			vec = np.arange(v, v + n - 1)
			grid[y, x:x+vec.shape[0]] = vec
		v += n - 1
		grid = np.rot90(grid)
	return _get_sides(grid, n - 2, maxval, v, x+1, y+1)

def make_goal(size):
	maxval = pow(size, 2) - 1
	grid = np.zeros((size, size), dtype=np.uint8)
	return _get_sides(grid, size, maxval)

def get_goal_dict(goal, size):
	goal_dict = {}
	for y in range(size):
		for x in range(size):
			goal_dict[str(goal[y, x])] = (x, y)
	return goal_dict


class Goal():
	def __init__(self, size):
		self.state = make_goal(size)
		self.list = self.state.tolist()
		self.tuple_1D = tuple(self.state.flatten())
		self.idx_dict = get_goal_dict(self.state, size)
		self.tuple_2D = tuple(map(tuple, self.list))

		# self.str = str(tuple(self.state.flatten()))
		self.list_str = str(self.list)
		self.str = self.list_str
		print(f'self.tuple_1D : {self.tuple_1D}')
		print(f'self.tuple_2D : {self.tuple_2D}')
		print(f'self.str : {self.str}')
		print(f'self.list_str : {self.list_str}')

	def __str__(self):
		return self.str
