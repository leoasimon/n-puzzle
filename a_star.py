from heuristics import get_h_score
from printer import print_solution, get_path
from goal import Goal
import numpy as np
import heapq

import sys

def get_empty_coords(grid, size):
	for y in range(size):
		for x in range(size):
			if grid[y][x] == 0:
				return (y, x)

def get_swap(grid, ax, ay, bx, by, s):
	if by == s or by < 0 or bx == s or bx < 0:
		return None
	lst = [[x for x in row] for row in grid]
	tmp = lst[by][bx]
	lst[ay][ax] = tmp
	lst[by][bx] = 0
	return tuple([tuple(l) for l in lst])

def get_neighbors(grid, size):
	y, x = get_empty_coords(grid, size)
	u = get_swap(grid, x, y, x, y + 1, size)
	r = get_swap(grid, x, y, x - 1, y, size)
	d = get_swap(grid, x, y, x, y - 1, size)
	l = get_swap(grid, x, y, x + 1, y, size)
	return [e for e in [u,r,d,l] if e is not None]


class NodeList():
	"""Contains opened queue and game statistics"""

	def __init__(self, options=[]):
		self.opened = []

		#TODO: Move stats?
		self.size = 0
		self.max_open = 0
		self.total_open = 0
		self.total_popped = 0
		self.moves = 0
		self.g_increase = 1 if "greedy" not in options else 0

	def push_node(self, f_score, state):
		heapq.heappush(self.opened, (f_score, state))
		self.total_open += 1

	def pop_node(self):
		_, state = heapq.heappop(self.opened)
		self.max_open = max(self.max_open, len(self.opened))
		self.total_popped += 1
		return state

def solve(a, size, options):
	a = tuple(map(tuple, a))
	
	goal = Goal(size)
	opensq = NodeList()

	g_scores = {}
	f_scores = {}
	parents = {}

	parents[a] = None
	g_scores[a] = 0
	f_scores[a] = get_h_score(a, goal.tuple_2D, goal.idx_dict, size, options)

	if a == goal.tuple_2D:
		print(f'Found solution with 0 moves.')
		return print_solution(a, parents, 0)

	opensq.push_node(f_scores[a], a)

	while len(opensq.opened):
		curr = opensq.pop_node()
		neighbors = get_neighbors(curr, size)
		g = g_scores[curr] + opensq.g_increase

		for n in neighbors:
			if n == goal.tuple_2D:
				parents[n] = curr
				print(f'Found solution with {g if "greedy" not in options else opensq.total_popped} moves.')
				return print_solution(n, parents, 0)

			if n not in g_scores:
				h = get_h_score(n, goal.state, goal.idx_dict, size, options)
				f_scores[n] = h + g
			elif g < g_scores[n]:
				f_scores[n] -= g_scores[n] - g
			else:
				continue
			parents[n] = curr
			g_scores[n] = g
			opensq.push_node(f_scores[n], n)

	