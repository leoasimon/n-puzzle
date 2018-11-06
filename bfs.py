import numpy as np
from collections import deque

def get_swap(grid, ax, ay, bx, by, s):
	if by == s or by < 0 or bx == s or bx < 0:
		return None
	inc = 1 if grid[by, bx] > -1 else 0
	grid_copy = np.array(grid)
	grid_copy[ay, ax] = grid[by, bx]
	grid_copy[by, bx] = -1
	return (grid_copy, inc, (bx, by))

def get_neighbors(grid, size, x, y):
	u = get_swap(grid, x, y, x, y + 1, size)
	r = get_swap(grid, x, y, x - 1, y, size)
	d = get_swap(grid, x, y, x, y - 1, size)
	l = get_swap(grid, x, y, x + 1, y, size)
	return [e for e in [u,r,d,l] if e is not None]

def build_key(arr, nums):
	key = ""
	for n in nums:
		y, x = np.where(arr == n)
		if len(x) and len(y):
			key += str(x[0]) + str(y[0])
		else:
			key += "-1-1"
	return key

def bfs(goal, size, start_coords):
	db = {}
	nums = [e for e in goal.flatten() if e != -1]

	start_str = tuple(goal.flatten())
	start = (start_str, start_coords)

	closed = set()
	opens = deque()
	opens.append(start)
	g_scores = {start_str: 0}

	i = 0
	while opens:
		curr_str, (blank_x, blank_y) = opens.popleft()
		curr = np.asarray(curr_str).reshape(size, size)
		neighbors = get_neighbors(curr, size, blank_x, blank_y)
		for n in neighbors:
			n, inc, b_coords = n
			n_str = tuple(n.flatten())
			if (n_str, b_coords) in closed:
				continue
			if (n_str, b_coords) not in opens:
				g_score = g_scores[curr_str] + inc
				if n_str not in g_scores or g_scores[n_str] > g_score:
					g_scores[n_str] = g_score
				opens.append((n_str, b_coords))
		closed.add((curr_str, (blank_x, blank_y)))
		key = build_key(curr, nums)
		db[key] = g_scores[curr_str]
		i += 1
	return db