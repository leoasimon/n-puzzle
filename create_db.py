#! /usr/bin/env python3
# 
from heuristics import get_h_score
from printer import print_solution, get_path
from goal import make_goal, get_goal_dict
import numpy as np
from collections import deque
import json

try:
	import Queue as Q  # ver. < 3.0
except ImportError:
	import queue as Q

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
	return [e for e in [u,r,d,l] if e is not None]

def build_key(arr, nums):
	key = ""
	for n in nums:
		y, x = np.where(arr == n)
		if len(x) and len(y):
			key += str(x[0]) + str(y[0])
	return key

# def createDb():
# 	size = 4
# 	a = np.array([
# 		[1,-1,-1,-1],
# 		[12,13,-1,-1],
# 		[11,-1,-1,-1],
# 		[10,9,-1,-1],
# 	])
# 	b = np.array([
# 		[-1,2,3,4],
# 		[-1,-1,-1,-1],
# 		[-1,-1,-1,-1],
# 		[-1,-1,-1,-1],
# 	])
# 	c = np.array([
# 		[-1,-1,-1,-1],
# 		[-1,-1,14,5],
# 		[-1,-1,15,6],
# 		[-1,-1,8,7],
# 	])
# 	grid = make_goal(size)
# 	closed = set()
	
# 	grid_str = tuple(grid.flatten())
# 	opens = deque()
# 	opens.append(grid_str)
# 	g_scores = {grid_str: 0}
# 	goals = [a,b,c]

# 	i = 0
# 	while opens:
# 		curr_str = opens.popleft()
# 		curr = np.asarray(curr_str).reshape(size, size)
# 		neighbors = get_neighbors(curr, size)
# 		for n in neighbors:
# 			n_str = tuple(n.flatten())
# 			if n_str in closed:
# 				continue
# 			if n_str not in opens:
# 				g_scores[n_str] = g_scores[curr_str] + 1
# 				opens.append(n_str)
# 		closed.add(curr_str)
# 		i += 1
	

# 	dbs = [{},{},{}]
# 	nums_a = [e for e in a.flatten() if e != -1]
# 	nums_b = [e for e in b.flatten() if e != -1]
# 	nums_c = [e for e in c.flatten() if e != -1]
# 	nums_all = [nums_a, nums_b, nums_c]
# 	for e_str in closed:
# 		e = np.asarray(e_str).reshape(size, size)
# 		score = g_scores[e_str]
# 		for i, g, nums in zip(range(3), goals, nums_all):
# 			db = dbs[i]
# 			t = np.where(g != -1, e, -1)
# 			key = build_key(t, nums)
# 			if key in db and db[key] < score:
# 				continue
# 			db[key] = score
	
# 	for db, name in zip(dbs, ["4x4_a", "4x4_b", "4x4_c"]):
# 		with open(name, "w") as f:
# 			jf = json.dumps(db)
# 			f.write(jf)

def createDb():
	size = 2
	a = np.array([
		[1,2],[-1,-1]
	])
	b = np.array([
		[-1,-1],[0,-1]
	])
	c = np.array([
		[-1,-1],[-1,3]
	])
	grid = make_goal(size)
	closed = set()
	
	grid_str = tuple(grid.flatten())
	opens = deque()
	opens.append(grid_str)
	g_scores = {grid_str: 0}
	goals = [a,b,c]

	i = 0
	while opens:
		curr_str = opens.popleft()
		curr = np.asarray(curr_str).reshape(size, size)
		neighbors = get_neighbors(curr, size)
		for n in neighbors:
			n_str = tuple(n.flatten())
			if n_str in closed:
				continue
			if n_str not in opens:
				g_scores[n_str] = g_scores[curr_str] + 1
				opens.append(n_str)
		closed.add(curr_str)
		i += 1
	

	dbs = [{},{},{}]
	nums_a = [e for e in a.flatten() if e != -1]
	nums_b = [e for e in b.flatten() if e != -1]
	nums_c = [e for e in c.flatten() if e != -1]
	nums_all = [nums_a, nums_b, nums_c]
	for e_str in closed:
		e = np.asarray(e_str).reshape(size, size)
		score = g_scores[e_str]
		for i, g, nums in zip(range(3), goals, nums_all):
			db = dbs[i]
			t = np.where(g != -1, e, -1)
			key = build_key(t, nums)
			if key in db and db[key] < score:
				continue
			db[key] = score
	
	for db, name in zip(dbs, ["4x4_a.json", "4x4_b.json", "4x4_c.json"]):
		with open(name, "w") as f:
			print(name)
			jf = json.dumps(db)
			f.write(jf)

if __name__ == "__main__":
	createDb()