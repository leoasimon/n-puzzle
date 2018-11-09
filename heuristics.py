import numpy as np
import operator

import sys

def get_linear_conflicts(grid, goal, goal_dict, size):
	sys.exit('LC not implemented without NP yet.')

def get_pattern_cost(grid, size):
	sys.exit('Pattern DB not implemented without NP yet.')


def get_misplaced_tiles(grid, goal):
	sys.exit('Misplaced tiles not implemented without NP yet.')

def get_manhattan(grid, goal, goal_dict, size):
	"""Get manhattan cost (with/without numpy)"""
	diff = 0
	for y in range(size):
		for x, val in enumerate(grid[y]):
			if val:
				goal_pos_x, goal_pos_y = goal_dict[str(val)]
				diff += abs(x - goal_pos_x) + abs(y - goal_pos_y)
	return diff

def get_h_score(grid, goal, goal_dict, size, options):
	if "mt" in options:
		return get_misplaced_tiles(grid, goal)
	elif "db" in options:
		return get_pattern_cost(grid, size)
	elif "lc" in options:
		m = get_manhattan(grid, goal, goal_dict, size) #TODO: remove, should all be in lc function
		return m + get_linear_conflicts(grid, goal, goal_dict, size)
	elif "mh" in options:
		return get_manhattan(grid, goal, goal_dict, size)
	else:
		return get_manhattan(grid, goal, goal_dict, size)