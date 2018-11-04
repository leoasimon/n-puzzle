#! /usr/bin/env python3

import numpy as np
from util import bcolors as col
from goal import make_goal
import sys

def _get_inversions(grid1D):
	if not len(grid1D):
		return 0
	inversions = 0
	for i, a in enumerate(grid1D):
		for j, b in enumerate(grid1D[i:]):
			if a > b and a > 0 and b > 0:
				inversions += 1
	return inversions

def get_valid(grid, size):
	# each legal vertical move changes total inversions, horizontal moves do not
	# if side polarity is odd:
		# tile X will pass an even no. of tiles if moved vertically
		# thus adding or subtracting an even number to total inversions
		# thus polarity of total inversions never changes
		# thus total inversions polarity MUST match polarity of total inversions at goal state 
	# if side polarity is even:
		# tile X will pass an odd no. of tiles if moved vertically
		# thus changing polarity of total inversions each time
		# so total inversion polarity if board is legal:
			# TODO: Placeholder, check if true
			# 1. MUST match polarity of total inversions at goal state IF blank tile starts AND ends on even row
			# 2. ELSE must NOT match polarity
	grid1D = grid.flatten()
	inversions_grid = _get_inversions(grid1D)

	size_odd = size & 1
	

	goal1D = make_goal(size).flatten()
	inversions_goal = _get_inversions(goal1D)

	if not size_odd: 
		blank_y = size - np.where(grid == 0)[0]
	return
	
if __name__ == "__main__":
	pass