from heuristics import get_h_score
from printer import print_solution, get_path
from goal import Goal
import numpy as np
import heapq

import sys

class Node():
	"""A convenient way of housing grid states
	
	TODO: Replace with NoNumpyNode once heuristics working
	or integrate"""
	def __init__(self, state):
		self.state = state
		self.str = str(tuple(self.state.flatten()))

	def __str__(self):
		return self.str

	def _get_empty_coords(self):
		pos_empty = np.where(self.state == 0)
		return tuple(z[0] for z in pos_empty) # note: returns y, x

	def _get_swap(self, ax, ay, bx, by, s):
		if by == s or by < 0 or bx == s or bx < 0:
			return None
		grid_copy = self.state.copy()
		grid_copy[ay, ax] = self.state[by, bx]
		grid_copy[by, bx] = 0
		return grid_copy

	def get_neighbors(self, size):
		y, x = self._get_empty_coords()
		u = self._get_swap(x, y, x, y + 1, size)
		r = self._get_swap(x, y, x - 1, y, size)
		d = self._get_swap(x, y, x, y - 1, size)
		l = self._get_swap(x, y, x + 1, y, size)
		return [e for e in [u,r,d,l] if e is not None]

class NoNumpyNode():
	"""NO NUMPY, but contains same props as np grid state."""
	def __init__(self, state):
		self.state = state
		self.str = str(tuple(map(tuple, state)))

	def _get_empty_coords(self):
		for i, row in enumerate(self.state):
			for j, val in enumerate(row):
				if val == 0:
					return (i, j)

	def _get_swap(self, ax, ay, bx, by, s):
		"""Get valid neighboring moves"""
		if by == s or by < 0 or bx == s or bx < 0:
			return None
		grid_copy = [row.copy() for row in self.state]
		grid_copy[ay][ax] = self.state[by][bx]
		grid_copy[by][bx] = 0
		return grid_copy

	def get_neighbors(self, size):
		"""Get valid neighboring moves"""
		y, x = self._get_empty_coords()
		u = self._get_swap(x, y, x, y + 1, size)
		r = self._get_swap(x, y, x - 1, y, size)
		d = self._get_swap(x, y, x, y - 1, size)
		l = self._get_swap(x, y, x + 1, y, size)
		return [e for e in [u,r,d,l] if e is not None]

	def __str__(self):
		return self.str


class NodeList():
	"""Contains opened queue and game statistics"""

	def __init__(self):
		self.opened = []

		#TODO: Move stats?
		self.size = 0
		self.max_open = 0
		self.total_open = 0
		self.total_popped = 0
		self.moves = 0

	def push_node(self, f_score, node):
		heapq.heappush(self.opened, (f_score, str(node), node.state))
		self.total_open += 1

	def pop_node(self):
		"""TODO: needs to return NoNumpyNode"""
		_, _, state = heapq.heappop(self.opened)
		self.max_open = max(self.max_open, len(self.opened))
		self.total_popped += 1
		return Node(state)

def solve(a, size, options):
	a = Node(a)
	goal = Goal(size)
	opensq = NodeList()

	g_scores = {}
	f_scores = {}
	parents = {}

	parents[a.str] = None
	g_scores[a.str] = 0
	f_scores[a.str] = get_h_score(a.state, goal.state, goal.idx_dict, size, options)

	if a.str == goal.str:
		print(f'Found solution with 0 moves.')
		return print_solution(a.str, parents, 0)

	opensq.push_node(f_scores[a.str], a)

	while len(opensq.opened):
		curr = opensq.pop_node()
		neighbors = curr.get_neighbors(size)
		g = g_scores[curr.str] + 1 if "greedy" not in options else 0

		for n in neighbors:
			n = Node(n)
			if n.str == goal.str:
				parents[n.str] = curr.str
				print(f'Found solution with {g if "greedy" not in options else opensq.total_popped} moves.')
				return print_solution(n.str, parents, 0)

			if n.str not in g_scores:
				h = get_h_score(n.state, goal.state, goal.idx_dict, size, options)
				f_scores[n.str] = h + g
			elif g < g_scores[n.str]:
				f_scores[n.str] -= g_scores[n.str] - g
			else:
				continue
			parents[n.str] = curr.str
			g_scores[n.str] = g
			opensq.push_node(f_scores[n.str], n)

	