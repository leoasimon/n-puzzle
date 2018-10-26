from heuristics import get_h_score
from printer import print_solution

def get_goal(size):
	#Todo: do real thing
	return (
		(1,2,3),
		(8,0,4),
		(7,6,5)
	)

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

def flatten(grid):
	return grid

def solve(a, size):
	opens = [a]
	print(size)
	closed = []
	g_scores = {}
	f_scores = {}
	parents = {}
	goal = get_goal(size)

	if get_is_goal(a, goal, size):
		print("Original grid matched goal!")
		sys.exit(0)

	goal_dict = get_goal_dict(goal, size)

	g_scores[a] = 0
	parents[a] = None
	f_scores[a] = get_h_score(a, goal_dict, size) # g (is 0) + h

	i = 1
	while opens:
		opens.sort(key=lambda e: f_scores[e])
		current = opens.pop(0) # TODO: use queue instead of list? (so we don't have to shift entire array)
		if get_is_goal(current, goal, size):
			print_solution(n, parents, i)
		closed.append(current)
		neighbors = get_neighbors(current, size)

		for n in neighbors:
			if n in closed:
				continue
			new_g = g_scores[current] + 1
			if n not in opens:
				opens.append(n)
			elif n in g_scores and new_g >= g_scores[n]:
				continue
			parents[n] = current
			g_scores[n] = new_g
			f_scores[n] = new_g + get_h_score(n, goal_dict, size)
		i += 1