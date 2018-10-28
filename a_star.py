from heuristics import get_h_score
from printer import print_solution, get_path
from generator import make_goal

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
	import queue as Q

def get_goal(size):
	#Todo: do real thing
	return make_goal(size)

def get_empty_coords(grid, size):
	for y in range(size):
		for x in range(size):
			if grid[x][y] == 0:
				return (x, y)

def get_swap(grid, ax, ay, bx, by, s):
	if by == s or by < 0 or bx == s or bx < 0:
		return
	lst = list(grid)
	lst = [list(e) for e in lst]
	tmp = lst[ax][ay]
	lst[ax][ay] = lst[bx][by]
	lst[bx][by] = tmp
	# print(lst)
	return tuple([tuple(l) for l in lst])

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

def get_is_goal(grid, goal, size):
	for y in range(size):
		for x in range(size):
			if grid[x][y] != goal[x][y]:
				return False
	return True

def solve(a, size):
	opens = [a]

	opensq = Q.PriorityQueue()

	print("Size: " + str(size))
	g_scores = {}
	f_scores = {}
	parents = {}
	closed = {}
	goal = get_goal(size)

	if get_is_goal(a, goal, size):
		print("Original grid matched goal!")
		sys.exit(0)

	goal_dict = get_goal_dict(goal, size)

	g_scores[a] = 0
	parents[a] = None

	f_scores[a] = get_h_score(a, goal, goal_dict, size)

	opensq.put((f_scores[a], a))

	i = 1
	while not opensq.empty():
		current = opensq.get()[1]
		neighbors = get_neighbors(current, size)
		g = g_scores[current] + 1

		for n in neighbors:
			if n == goal:
				parents[n] = current
				return get_path(n, parents, 0)

			if n not in g_scores or g < g_scores[n]:
				if n in closed:
					print(f'n in closed: {i}')
				parents[n] = current
				g_scores[n] = g
				f_scores[n] = get_h_score(n, goal, goal_dict, size) + g
				opensq.put((f_scores[n], n))

		closed[current] = f_scores[n]
		i += 1