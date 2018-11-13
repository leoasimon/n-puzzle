from heuristics import get_h_score
from printer import print_solution, get_path
from goal import Goal
import numpy as np
import heapq

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
	return [Node(e) for e in [u,r,d,l] if e is not None]

class Node():
	"""A convenient way of housing grid states"""
	def __init__(self, state):
		self.state = state
		self.tup = tuple(self.state.flatten())

	def __lt__(self, other):
		return self.tup < other.tup

class Stats():
	"""Contains solver statistics"""

	def __init__(self, size, algo="astar", heuristic="manhattan"):
		self.size = size
		self.algo = algo
		self.heuristic = heuristic
		self.max_open = 0 # max number of nodes in opened queue (space complexity)
		self.total_open = 0 # how many times we added to opened queue (time complexity)
		self.total_popped = 0 # how many nodes we (re-)evaluated
		self.moves = 0

	def increase_total_added(self):
		self.total_open += 1

	def update_max_open(self, other):
		self.max_open = max(self.max_open, other)

	def increase_total_popped(self):
		self.total_popped += 1

	def set_moves(self, num_moves=None):
		if self.algo == "greedy":
			self.moves = self.total_popped
		else:
			self.moves = num_moves

class Search():
	"""Contains opened queue"""

	def __init__(self, size, options={}):
		self.opened = []
		self.algo = options.algorithm
		self.labels = {
			"lc": "Manhattan distance + linear conflict",
			"mh": "Manhattan distance",
			"mt": "Misplaced tiles",
			"db": "Pattern database",
		}
		self.heuristic = self.labels[options.heuristic]
		self.stats = Stats(size, self.algo, self.heuristic)

	def push_node(self, f_score, node):
		heapq.heappush(self.opened, (f_score, node))
		self.stats.increase_total_added()
		self.stats.update_max_open(len(self.opened))

	def pop_node(self):
		node = heapq.heappop(self.opened)[1]
		self.stats.increase_total_popped()
		return node

def solve(a, size, options, dbs):
	a = Node(a)
	goal = Goal(size)
	search = Search(size, options)

	g_scores = {}
	f_scores = {}
	parents = {}

	parents[a.tup] = None
	g_scores[a.tup] = 0
	f_scores[a.tup] = get_h_score(a.state, goal.state, goal.idx_dict, size, options, dbs)

	search.push_node(f_scores[a.tup], a)

	if np.array_equal(a.state, goal.state):
		return print_solution(search.stats, a.tup, parents, 0)

	while len(search.opened):
		curr = search.pop_node()
		neighbors = get_neighbors(curr.state, size)
		g = g_scores[curr.tup] + 1 if search.algo == "astar" else 0

		for n in neighbors:
			if n.tup == goal.tup:
				parents[n.tup] = curr.tup
				search.stats.set_moves(g)
				return print_solution(search.stats, n.tup, parents, 0)

			if n.tup not in g_scores:
				h = get_h_score(n.state, goal.state, goal.idx_dict, size, options, dbs)
				f_scores[n.tup] = h + g
			elif g < g_scores[n.tup]:
				f_scores[n.tup] -= g_scores[n.tup] - g
			else:
				continue
			parents[n.tup] = curr.tup
			g_scores[n.tup] = g
			search.push_node(f_scores[n.tup], n)

	