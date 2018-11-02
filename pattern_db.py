#! /usr/bin/env python3
# 
from a_star import solve, get_empty_coords, get_neighbors
from printer import print_solution
from goal import get_goal_dict, make_goal
from parser import parse
import heapq

import sys
import os

import numpy as np

file1 = "tests/puzzles/valids/hard_3x3"

class Node:
	def __init__(self, grid, cost, size):
		self.st = grid.copy()
		self.cost = cost
		self.y, self.x = get_empty_coords(grid)

	def __str__(self):
		return np.array_str(self.st)

	def __lt__(self, other):
		return self.cost < other.cost

class Entry:
	def __init__(self, node):
		self.st = str(node)
		self.cost = node.cost

if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.argv.append(file1)
	target, size, options = parse()
	final = make_goal(3)


	# start breadth-first search (start at goal)
		# add to queue in order of lowest cost
	# add state and cost to DB only when cost changes and cost is less than DB entry if it exists
	# finish when all pieces in right position

