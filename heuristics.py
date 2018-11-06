import numpy as np
import scipy.spatial.distance
import operator

from create_db import get_goals, get_db
from bfs import build_key

def get_lc_line(row, goal_row):
	conflicts = []
	counts = {}
	for i, tj in enumerate(row[1:]):
		if tj not in goal_row:
			continue
		for tk in row[0:i+1]:
			if tk not in goal_row:
				continue
			gtk = goal_row.index(tk)
			gtj = goal_row.index(tj)
			if gtk > gtj:
				conflicts.append((tj, tk))
	for e in row:
		for c in conflicts:
			if c[0] == e:
				if e not in counts:
					counts[e] = 0
				counts[e] +=1
	if not counts:
		return 0
	m = max(counts.items(), key=operator.itemgetter(1))[0]
	return sum([v - 1 for v in counts.values()]) + 1

def get_linear_conflicts(grid, goal, goal_dict, size):
	#Ugly and slow
	diff = 0
	for i in range(size):
		col = grid[:,i]
		row = grid[i,:]
		goal_col = goal[:,i]
		goal_row = goal[i,:]
		diff += get_lc_line(list(row), list(goal_row))
		diff += get_lc_line(list(col), list(goal_col))
	return diff * 2

#Todo: store db somewhere so we don't have to open the file any times
def get_pattern_cost(grid, size):
	diff = 0
	goals = get_goals(size)
	for g, name in zip(goals, ['a', 'b', 'c']):
		nums = [e for e in g.flatten() if e != -1]
		filtered = np.where(g != 0, grid, -1)
		key = build_key(filtered, nums)
		db = get_db(size, name)
		diff += db[key] if key in db else 0
	return diff

def get_manhattan(grid, goal, goal_dict, size):
	diff = 0
	# TODO: Try iterators instead...? I tried this, but it doesn't seem faster	
	# it = np.nditer(grid, flags=['multi_index'])
	# while not it.finished:
	# 	goal_pos_x, goal_pos_y = goal_dict[str(it[0])]
	# 	diff += abs(it.multi_index[0] - goal_pos_y) + abs(it.multi_index[1] - goal_pos_x)
	# 	it.iternext()

	# Without iterators:
	for y in range(size):
		for x, val in enumerate(grid[y]):
			if val:
				goal_pos_x, goal_pos_y = goal_dict[str(val)]
				diff += abs(x - goal_pos_x) + abs(y - goal_pos_y)
	return diff

def get_h_score(grid, goal, goal_dict, size, options):
	if "db" in options:
		return get_pattern_cost(grid, size)
	m = get_manhattan(grid, goal, goal_dict, size)
	if "lc" in options:
		return m + get_linear_conflicts(grid, goal, goal_dict, size)
	return m