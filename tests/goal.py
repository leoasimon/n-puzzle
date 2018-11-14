#! /usr/bin/env python3

from os import getcwd
from os.path import join
import sys
import unittest
sys.path.insert(0, join(getcwd(), "../"))
import numpy as np

from goal import Goal

def fold(grid, l, size, off=0):
	if not len(l):
		return grid
	if grid[off, off] > -1: # move inward
		off += 1
		size -= 2
		if (size == 1):
			grid[off, off] = l[0]
			return grid
		elif size == 0:
			return grid
	grid[off, off:off+size-1] = l[0:size-1]
	return fold(np.rot90(grid), l[size-1:], size, off)

def unfold(grid, size):
	if grid.size == 1:
		return [grid[0, 0]]
	top = grid[0].tolist()
	l = top + unfold(np.rot90(grid[1:]), size-1)
	return l

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GoalTest(unittest.TestCase):
	def test_all_ints_in_range_on_board(self):
		for i in range(3, 15):
			with self.subTest(i=i):
				g = Goal(i)
				tf = g.state.flatten()
				self.assertTrue(np.array_equal(np.sort(tf), np.arange(pow(int(i), 2), dtype=np.uint8)), msg='Not all ints are present on some.')

	def test_all_ints_contiguous(self):
		for i in range(3, 15):
			with self.subTest(i=i):
				g = Goal(i)
				r = np.arange(pow(int(i), 2), dtype=np.uint8)
				r = r[r>0]
				unfolded = np.array(unfold(g.state, i))
				unfolded = unfolded[unfolded>0]
				self.assertTrue(np.array_equal(r, unfolded), msg='Not all ints are contiguous.')
	
if __name__ == '__main__':
	if '-v' not in sys.argv:
		print(f'{bcolors.OKBLUE} Recommended usage: ./goal.py -v {bcolors.ENDC}')
	unittest.main()