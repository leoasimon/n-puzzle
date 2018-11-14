#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from bfs import build_key
from create_db import get_goals

def _get_lc_line(row, goal_row):
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
	return sum([v - 1 for v in counts.values()]) + 1

def get_linear_conflicts(grid, goal, goal_dict={}, size=None, dbs=[], goals=[]):
	lc = 0
	m = 0
	for i in range(size):
		col = grid[:,i]
		row = grid[i,:]
		goal_col = goal[:,i]
		goal_row = goal[i,:]
		lc += _get_lc_line(list(row), list(goal_row))
		lc += _get_lc_line(list(col), list(goal_col))
		for x, val in enumerate(row):
			if val:
				goal_pos_x, goal_pos_y = goal_dict[str(val)]
				m += abs(x - goal_pos_x) + abs(i - goal_pos_y)
	return m + (lc * 2)

def get_pattern_cost(grid, goal, goal_dict={}, size=None, dbs=[], goals=[]):
	diff = 0
	goals = get_goals(size)
	for g, db in zip(goals, dbs):
		nums = [e for e in g.flatten() if e != -1]
		filtered = np.where(g != 0, grid, -1)
		key = build_key(filtered, nums)
		diff += db[key] if key in db else 0
	return diff

def get_misplaced_tiles(grid, goal, goal_dict={}, size=None, dbs=[], goals=[]):
	filtered = np.where(grid != goal)
	if np.where(grid == 0) != np.where(goal == 0):
		return len(filtered[0]) - 1
	return len(filtered[0])

def get_manhattan(grid, goal, goal_dict, size, dbs=[], goals=[]):
	diff = 0
	for y in range(size):
		for x, val in enumerate(grid[y]):
			if val:
				goal_pos_x, goal_pos_y = goal_dict[str(val)]
				diff += abs(x - goal_pos_x) + abs(y - goal_pos_y)
	return diff