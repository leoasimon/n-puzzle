#! /usr/bin/env python3

import sys
import re

def get_int_lst(l):
	return [int(e) for e in l]

def parse():
	lines = [l.split() for l in sys.stdin if l[0] != "#"]
	size = int(lines.pop(0)[0])

	print("size : {}".format(size))
	lines = [get_int_lst(l) for l in lines]
	return (tuple([tuple(l) for l in lines]), size)

def get_goal(size):
	return (
		(1,2,3),
		(8,0,4),
		(7,6,5)
	)

def print_grid(grid):
	for line in grid:
		print(line)

def get_empty_coords(grid, size):
	for y in range(size):
		for x in range(size):
			if grid[x][y] == 0:
				return (x, y)

def get_swap(grid, ax, ay, bx, by, s):
	if by == size or by < 0 or bx == size or bx < 0:
		return
	lst = list(grid)
	lst = [list(e) for e in lst]
	tmp = lst[ax][ay]
	lst[ax][ay] = lst[bx][by]
	lst[bx][by] = tmp
	# print(lst)
	return tuple([tuple(l) for l in lst])

def get_neighbors(grid, size):
	x, y = get_empty_coords(grid, size)
	u = get_swap(grid, x, y, x, y + 1, size)
	r = get_swap(grid, x, y, x - 1, y, size)
	d = get_swap(grid, x, y, x, y - 1, size)
	l = get_swap(grid, x, y, x + 1, y, size)
	return [e for e in [u,r,d,l] if e]

# dict of tuples representing (x, y) of each goal grid value
def get_goal_dict(goal, size):
	goal_dict = {}
	for y in range(size):
		for x in range(size):
			goal_dict[str(goal[y][x])] = (x, y)
	return goal_dict

def get_manhattan(grid, goal_dict, size): # TODO: Haven't tested
	diff = 0
	for y in range(size):
		for x in range(size):
			grid_val = grid[y][x]
			goal_pos_x, goal_pos_y = goal_dict[str(grid_val)]
			distance_x = abs(x - goal_pos_x)
			distance_y = abs(y - goal_pos_y)
			diff += distance_x + distance_y
	return diff

def get_is_goal(grid, goal, size):
	for y in range(size):
		for x in range(size):
			if grid[x][y] != goal[x][y]:
				return False
	return True

def flatten(grid):
	grid_key = ''
	for line in grid:
		grid_key += ''.join(str(x) for x in line)
	return grid_key

if __name__ == '__main__':
	a, size = parse()
	opens = [a]
	closed = []
	g_scores = {}
	f_scores = {}
	parents = {}
	goal = get_goal(size)
	a_key = flatten(a)

	if get_is_goal(a, goal, size):
		print("Original grid matched goal!")
		sys.exit(0)

	goal_dict = get_goal_dict(goal, size)

	g_scores[a_key] = 0
	parents[a_key] = None
	f_scores[a_key] = get_manhattan(a, goal_dict, size) # g (is 0) + h

	i = 1
	while opens and i < 100000:
		current = opens.pop(0) # TODO: use queue instead of list? (so we don't have to shift entire array)
		closed.append(current)
		neighbors = get_neighbors(current, size)

		min_neighbor = neighbors[0]

		for n in neighbors:
			n_key = flatten(n)

			if get_is_goal(n, goal, size):
				print("Got to goal after " + str(i) + " searches.")
				sys.exit(0)
			if n in closed:
				g_scores[n_key] = min([i, g_scores[n_key]])
				# TODO: update f_score
			else:
				parents[n_key] = current
				g_scores[n_key] = i
				f_scores[n_key] = i + get_manhattan(n, goal_dict, size)
			if f_scores[n_key] < f_scores[flatten(min_neighbor)]:
				min_neighbor = n
		opens.append(min_neighbor)

		i += 1
		