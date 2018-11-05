#! /usr/bin/env python3

import numpy as np
from goal import make_goal
import sys

def _get_inversions(grid1D):
	if not len(grid1D):
		return 0
	inversions = 0
	for i, a in enumerate(grid1D):
		for b in grid1D[i:]:
			if a > b and a > 0 and b > 0:
				inversions += 1
	return inversions

def get_valid(grid, size):
	# each legal vertical move changes total inversions, horizontal moves do not
	# vertical moves change polarity of total inversions only if board width is odd
	# http://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
	grid1D = grid.flatten()
	inversions_grid = _get_inversions(grid1D)

	side_odd = bool(size & 1)
	goal = make_goal(size)
	
	goal1D = goal.flatten()
	inversions_goal = _get_inversions(goal1D)

	if not side_odd: 
		blank_row_start = size - np.where(grid == 0)[0]
		blank_row_goal = size - np.where(goal == 0)[0]

		# compensate for variable goal row polarity in spiral board
		inversions_goal += blank_row_goal & 1
		inversions_grid += blank_row_start & 1
	return bool(inversions_grid & 1) == (inversions_goal & 1)
	
if __name__ == "__main__":
	pass