from heuristics import get_h_score
from printer import print_solution, get_path
from goal import make_goal, get_goal_dict
import numpy as np

try:
	import Queue as Q  # ver. < 3.0
except ImportError:
	import queue as Q

def get_empty_coords(grid):
	pos_empty = np.where(grid == 0)
	return tuple(z[0] for z in pos_empty) # note: returns y, x

def get_swap(grid, ax, ay, bx, by, s):
	if by == s or by < 0 or bx == s or bx < 0:
		return None
	grid_copy = np.array(grid)
	grid_copy[ay, ax] = grid[by, bx]
	grid_copy[by, bx] = 0
	return grid_copy

def get_neighbors(grid, size):
	y, x = get_empty_coords(grid)
	u = get_swap(grid, x, y, x, y + 1, size)
	r = get_swap(grid, x, y, x - 1, y, size)
	d = get_swap(grid, x, y, x, y - 1, size)
	l = get_swap(grid, x, y, x + 1, y, size)
	return [e for e in [u,r,d,l] if e is not None]

def createDb():
	size = 4
	goal = np.array([
		[1,-1,-1,-1],
		[12,15,-1,-1],
		[11,0,-1,-1],
		[10,9,-1,-1],
	])
	goal_str = tuple(goal.flatten())
	
	a = goal
	a_str = goal_str

	# print(f'a_str : {a_str}')
	opens = [a]
	h_scores = {}
	goal_dict = get_goal_dict(goal, size)

	while opens:
		curr = opens.pop(0)
		neighbors = get_neighbors(curr, size)

		for n in neighbors:
			n_str = n.flatten()
			n_str = tuple(n.flatten())
			if n_str not in h_scores:
				h_scores[n_str] = get_h_score(n, goal, goal_dict, size, [])
				opens.append(n)
	print("yeah")