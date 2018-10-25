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

if __name__ == '__main__':
	a, size = parse()
	# print(a)
	opens = [a]
	closed = []
	g_scores = []
	f_scores = []
	parents = []
	goal = get_goal(size)
	# print(goal)

	while opens:
		current = opens.pop(0)
		closed.append(current)
		neighbors = get_neighbors(current, size)
		for n in neighbors:
			print(n)