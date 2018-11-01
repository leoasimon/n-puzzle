from heuristics import get_h_score
from printer import print_solution, get_path
from generator import make_goal
import numpy as np
import sys

try:
	import Queue as Q  # ver. < 3.0
except ImportError:
	import queue as Q

def get_goal(size) -> np.matrix:
	return make_goal(size)

def get_empty_coords(grid, size):
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
	y, x = get_empty_coords(grid, size)
	u = get_swap(grid, x, y, x, y + 1, size)
	r = get_swap(grid, x, y, x - 1, y, size)
	d = get_swap(grid, x, y, x, y - 1, size)
	l = get_swap(grid, x, y, x + 1, y, size)
	return [e for e in [u,r,d,l] if e is not None]

# dict of tuples representing (x, y) of each goal grid value
def get_goal_dict(goal, size):
	goal_dict = {}
	for y in range(size):
		for x in range(size):
			goal_dict[str(goal[y, x])] = (x, y)
	return goal_dict

def solve(a, size):
	a = np.array(a, dtype=np.uint8)
	a_str = tuple(a.flatten())

	# print(f'a_str : {a_str}')
	opensq = Q.PriorityQueue()

	g_scores = {}
	f_scores = {}
	parents = {}
	goal = np.array(get_goal(size), dtype=np.uint8)
	goal_str = tuple(goal.flatten())
	goal_dict = get_goal_dict(goal, size)

	parents[a_str] = None
	g_scores[a_str] = 0

	h = get_h_score(a, goal, goal_dict, size)
	f_scores[a_str] = h

	if np.array_equal(a, goal):
		print(f'Found solution with 0 moves.')
		return print_solution(a_str, parents, 0)

	opensq.put((f_scores[a_str], a_str, a))
	
	opened = set()
	opened.add(a_str)
	closed = set()
	print(f'opened: {opened}')

	i = 1
	j = 1
	len_opensq = 1
	len_open_set = 1
	max_h_score = h
	max_f_score = f_scores[a_str]
	while not opensq.empty():
		_, curr_str, curr = opensq.get()
		if curr_str in opened: 
			opened.remove(curr_str)
		closed.add(curr_str)

		neighbors = get_neighbors(curr, size)
		g = g_scores[curr_str] + 1

		# print(f'sum([i for i in range[size * size]]): {sum(i for i in range(size * size))}')
		# print(f'size * size: {size * size}')
		# print(f'size * size * size: {size * size * size}')
		

		for n in neighbors:
			j += 1
			n_str = tuple(n.flatten())

			if n_str == goal_str:
				parents[n_str] = curr_str
				print(f'Found solution with {g} moves.')
				print(f'j: {j}')
				print(f'max_f_score: {max_f_score}')
				print(f'max_h_score: {max_h_score}')
				return print_solution(n_str, parents, 0)

			if n_str not in g_scores or g < g_scores[n_str]:
				parents[n_str] = curr_str
				g_scores[n_str] = g
				h = get_h_score(n, goal, goal_dict, size)
				f_scores[n_str] = h + g
				opensq.put((f_scores[n_str], n_str, n))
				len_opensq = max(opensq.qsize(), len_opensq)
				len_open_set = max(len(opened), len_open_set)
				max_f_score = max((f_scores[n_str], max_f_score))
				max_h_score = max((max_h_score, h))

		# print(f'\nlen_opensq: {len_opensq}')
		# print(f'len_open_set: {len_open_set}')
		# print(f'max_f_score: {max_f_score}')
		# print(f'max_h_score: {max_h_score}')
		# sys.exit()
		i += 1
	
