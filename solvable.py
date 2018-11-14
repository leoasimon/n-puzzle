#! /usr/bin/env python3

import numpy as np
from goal import make_goal
from error import PuzzleProblem

def _get_inversions(grid1D):
	if not len(grid1D):
		return 0
	inversions = 0
	for i, a in enumerate(grid1D):
		for b in grid1D[i:]:
			if a > b and a > 0 and b > 0:
				inversions += 1
	return inversions

def _change_inversions(grid):
	"""Updates board in-place so that total inversions is increased or decreased by 1"""
	a,b = np.dstack(np.where(grid > 0))[0][:2]
	tmp = grid[tuple(a)]
	grid[tuple(a)] = grid[tuple(b)]
	grid[tuple(b)] = tmp

def get_solvable(grid, size):
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

def generate_solvable(size):
	if size > 15 or size < 3:
		raise PuzzleProblem('Invalid puzzle size. Must be between 3-15.')
	puzzle = np.arange(size ** 2).reshape(size, size)
	if not get_solvable(puzzle, size):
		_change_inversions(puzzle)
	return puzzle