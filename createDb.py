from heuristics import get_h_score
from printer import print_solution, get_path
from goal import make_goal, get_goal_dict
import numpy as np
from collections import deque

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
	a = np.array([
		[1,-1,-1,-1],
		[12,13,-1,-1],
		[11,-1,-1,-1],
		[10,9,-1,-1],
	])
	b = np.array([
		[-1,2,3,4],
		[-1,-1,-1,-1],
		[-1,-1,-1,-1],
		[-1,-1,-1,-1],
	])
	c = np.array([
		[-1,-1,-1,-1],
		[-1,-1,14,5],
		[-1,-1,15,6],
		[-1,-1,8,7],
	])
	grid = np.array([
		[1,2,3,4],
		[12,13,14,5],
		[11,0,15,6],
		[10,9,8,7],
	])
	
	closed = set()
	
	grid_str = tuple(grid.flatten())
	opens = deque()
	opens.append(grid_str)
	g_scores = {grid_str: 0}
	goals = [a,b,c]

	i = 0
	while opens:
		curr_str = opens.popleft()
		curr = np.asarray(curr_str).reshape(size, size)
		neighbors = get_neighbors(curr, size)
		for n in neighbors:
			n_str = tuple(n.flatten())
			if n_str in closed:
				continue
			if n_str not in opens:
				opens.append(n_str)
				for g in goals:
					filtered = np.where(n == g, g, -1)
					if not np.array_equal(filtered, g):
						s = np.where(g != -1, n, -1)
						g_score = g_scores[curr_str] + 1
						s_key = tuple(s.flaten())
						if s_key not in g_scores or g_score < g_scores[s_key]:
							g_scores[s_key] = g_score
							opens.append(n)
		closed.add(curr_str)
		i += 1