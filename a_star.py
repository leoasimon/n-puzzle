from heuristics import get_h_score
from printer import print_solution, get_path
from generator import make_goal

try:
	import Queue as Q  # ver. < 3.0
except ImportError:
	import queue as Q

def get_goal(size):
	return make_goal(size)

def get_empty_coords(grid, size):
	for y in range(size):
		for x in range(size):
			if grid[y][x] == 0:
				return (x, y)

def get_swap(grid, ax, ay, bx, by, s):
	if by == s or by < 0 or bx == s or bx < 0:
		return None
	lst = list(grid)
	lst = [list(e) for e in lst]
	lst[ay][ax] = lst[by][bx]
	lst[by][bx] = 0
	return tuple(tuple(l) for l in lst)

def get_neighbors(grid, size):
	x, y = get_empty_coords(grid, size)
	u = get_swap(grid, x, y, x, y + 1, size)
	r = get_swap(grid, x, y, x - 1, y, size)
	d = get_swap(grid, x, y, x, y - 1, size)
	l = get_swap(grid, x, y, x + 1, y, size)
	return [e for e in [u,r,d,l] if e]

# dict of tuples representing (x, y) of each goal grid value
def get_goal_dict(goal, size):
	goal_dict = {}
	for y in range(size):
		for x in range(size):
			goal_dict[str(goal[y][x])] = (x, y)
	return goal_dict

def solve(a, size):
	opensq = Q.PriorityQueue()
	g_scores = {}
	f_scores = {}
	parents = {}
	goal = get_goal(size)
	goal_dict = get_goal_dict(goal, size)

	parents[a] = None
	g_scores[a] = 0
	f_scores[a] = get_h_score(a, goal, goal_dict, size)

	if a == goal:
		return get_path(a, parents, 0)

	opensq.put((f_scores[a], a))

	i = 1
	while not opensq.empty():
		current = opensq.get()[1]
		neighbors = get_neighbors(current, size)
		g = g_scores[current] + 1

		for n in neighbors:
			if n == goal:
				parents[n] = current
				return print_solution(n, parents, 0)

			if n not in g_scores or g < g_scores[n]:
				parents[n] = current
				g_scores[n] = g
				h = get_h_score(n, goal, goal_dict, size)
				f_scores[n] = h + g
				opensq.put((f_scores[n], n))
		i += 1