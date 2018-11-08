from heuristics import get_h_score
from printer import print_solution, get_path
from goal import make_goal, get_goal_dict
import numpy as np
import heapq

def get_goal(size):
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
	opensq = []
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

	heapq.heappush(opensq, (f_scores[a_str], a_str, a))

	max_opens = 1
	total_opens = 1
	times_updated_g_score = 0

	i = 1
	while len(opensq):
		_, curr_str, curr = heapq.heappop(opensq)
		neighbors = get_neighbors(curr, size)
		g = g_scores[curr_str] + 1 if "greedy" not in options else 0
		max_opens = max(len(opensq), max_opens)
		# print(f'{curr} .... {f_scores[curr_str]} [turn: {i}]\n')

		adding = len(neighbors)
		for n in neighbors:
			n_str = tuple(n.flatten())
			if n_str == goal_str:
				parents[n_str] = curr_str
				print(f'max_opens : {max_opens}')
				print(f'times_updated_g_score : {times_updated_g_score}')
				print(f'total_opens : {total_opens}')
				print(f'Found solution with {g if "greedy" not in options else i} moves.')
				return print_solution(n_str, parents, 0)

			if n_str not in g_scores: # O(1)
				h = get_h_score(n, goal, goal_dict, size, options)
				f_scores[n_str] = h + g
			elif g < g_scores[n_str]: #O(1)
				times_updated_g_score += 1
				# print(f'updating g score')
				f_scores[n_str] -= g_scores[n_str] - g
			else:
				adding -= 1
				continue
			parents[n_str] = curr_str
			g_scores[n_str] = g
			heapq.heappush(opensq, (f_scores[n_str], n_str, n)) # O(log n)
			total_opens += 1
		# print(f'---------- added {adding}; total: {len(opensq)}')
		i += 1

	