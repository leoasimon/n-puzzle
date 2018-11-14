#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class Goal():
	def __init__(self, size):
		self.size = size
		self.idx_dict = {}
		self.state = None
		self.tup = None

		self._make_goal()
		self._get_goal_dict()

	def _get_sides(self, grid, n, maxval, v=1, x=0, y=0):
		if v > maxval:
			return grid
	
		for _ in range(4):
			if v <= maxval:
				vec = np.arange(v, v + n - 1)
				grid[y, x:x+vec.shape[0]] = vec
			v += n - 1
			grid = np.rot90(grid)
		return self._get_sides(grid, n - 2, maxval, v, x+1, y+1)

	def _make_goal(self):
		maxval = pow(self.size, 2) - 1
		grid = np.zeros((self.size, self.size), dtype=np.uint8)
		self.state = self._get_sides(grid, self.size, maxval)
		self.tup = tuple(self.state.flatten())

	def _get_goal_dict(self):
		for t in self.tup:
			self.idx_dict[str(t)] = tuple(np.flip(np.dstack(np.where(self.state == t))[0][0]))