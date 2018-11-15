#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import heapq

import heuristics as he
from printer import print_solution
from goal import Goal
from create_db import get_dbs, get_goals

class Node():
	"""A convenient way of housing grid states"""
	def __init__(self, state):
		self.state = state
		self.tup = tuple(self.state.flatten())

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
		return [Node(e) for e in [u,r,d,l] if e is not None]

	def __lt__(self, other):
		return self.tup < other.tup

class Stats():
	"""Contains solver statistics"""

	def __init__(self, size, options):
		self.size = size
		self.algo = options.algorithm
		self.h_name = self._get_h_name(options.heuristic)
		
		self.max_open = 0 # max number of nodes in opened queue (space complexity)
		self.total_open = 0 # how many times we added to opened queue (time complexity)

	def increase_total_added(self):
		self.total_open += 1

	def update_max_open(self, other):
		self.max_open = max(self.max_open, other)

	def _get_h_name(self, heuristic):
		labels = {
			"lc": "Manhattan distance + linear conflict",
			"mh": "Manhattan distance",
			"mt": "Misplaced tiles",
			"db": "Pattern database",
		}
		return labels[heuristic]

class Search():
	"""Contains opened queue"""

	def __init__(self, size, options={}):
		self.opened = []
		self.algo = options.algorithm
		self.stats = Stats(size, options)
		self.h_fn = self.get_h_fn(options.heuristic)

	def push_node(self, f_score, node):
		heapq.heappush(self.opened, (f_score, node))
		self.stats.increase_total_added()
		self.stats.update_max_open(len(self.opened))

	def pop_node(self):
		node = heapq.heappop(self.opened)[1]
		return node

	def get_h_fn(self, heuristic):
		h_fns = {
			"lc": he.get_linear_conflicts,
			"mh": he.get_manhattan,
			"mt": he.get_misplaced_tiles,
			"db": he.get_pattern_cost
		}
		return h_fns[heuristic]

def solve(start, size, options):
	start = Node(start)
	goal = Goal(size)
	search = Search(size, options)

	goals = get_goals(size) if options.heuristic == 'db' else []
	dbs = get_dbs(size) if options.heuristic == 'db' else []

	g_scores = {}
	f_scores = {}
	parents = {}

	parents[start.tup] = None
	g_scores[start.tup] = 0
	f_scores[start.tup] = search.h_fn(start.state, goal.state, goal.idx_dict, size, dbs, goals)

	search.push_node(f_scores[start.tup], start)

	if np.array_equal(start.state, goal.state):
		return print_solution(search.stats, start.tup, parents, options)

	while len(search.opened):
		curr = search.pop_node()
		neighbors = curr.get_neighbors(size)
		g = g_scores[curr.tup] + 1 if search.stats.algo == "astar" else 0

		for n in neighbors:
			if n.tup == goal.tup:
				parents[n.tup] = curr.tup
				return print_solution(search.stats, n.tup, parents, options)

			if n.tup not in g_scores:
				h = search.h_fn(n.state, goal.state, goal.idx_dict, size, dbs, goals) if search.stats.algo != "uniform" else 0  
				f_scores[n.tup] = h + g
			elif g < g_scores[n.tup]:
				f_scores[n.tup] -= g_scores[n.tup] - g
			else:
				continue
			parents[n.tup] = curr.tup
			g_scores[n.tup] = g
			search.push_node(f_scores[n.tup], n)

	