from heuristics import get_h_score
from printer import print_solution, get_path
from goal import make_goal, get_goal_dict
import numpy as np

try:
	import Queue as Q  # ver. < 3.0
except ImportError:
	import queue as Q

def get_goal(size) -> np.matrix:
	return make_goal(size)

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

def solve(a, size, options):
	a_str = tuple(a.flatten())

	# print(f'a_str : {a_str}')
	opensq = Q.PriorityQueue()
	g_scores = {}
	f_scores = {}
	parents = {}
	goal = get_goal(size)
	goal_str = tuple(goal.flatten())
	goal_dict = get_goal_dict(goal, size)

	parents[a_str] = None
	g_scores[a_str] = 0
	f_scores[a_str] = get_h_score(a, goal, goal_dict, size, options)

	if np.array_equal(a, goal):
		print(f'Found solution with 0 moves.')
		return print_solution(a_str, parents, 0)

	opensq.put((f_scores[a_str], a_str, a))

	i = 1
	while not opensq.empty():
		_, curr_str, curr = opensq.get()
		neighbors = get_neighbors(curr, size)
		g = g_scores[curr_str] + 1

		for n in neighbors:
			n_str = tuple(n.flatten())
			if n_str == goal_str:
				parents[n_str] = curr_str
				print(f'Found solution with {g} moves.')
				return print_solution(n_str, parents, 0)

			if n_str not in g_scores:
				h = get_h_score(n, goal, goal_dict, size, options)
				f_scores[n_str] = h + g
			elif g < g_scores[n_str]:
				f_scores[n_str] -= g - g_scores[n_str]
			else:
				continue
			parents[n_str] = curr_str
			g_scores[n_str] = g
			opensq.put((f_scores[n_str], n_str, n))
		i += 1
