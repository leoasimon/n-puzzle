#! /usr/bin/env python3

from io import StringIO
from os import getcwd, listdir
from os.path import join, dirname, realpath
import sys
import subprocess
from unittest import TestCase
from unittest.mock import patch
import unittest as ut
sys.path.insert(0, join(getcwd(), "../"))
from parser import parsefile
import numpy as np

from solvable import _get_inversions, get_valid

dir_path = dirname(realpath(__file__))
p_path = join(dir_path, "../n-puzzle.py")

def _get_sides(grid, n, maxval, v=1, x=0, y=0):
	if v > maxval:
		return grid

	for _ in range(4):
		if v <= maxval:
			vec = np.arange(v, v + n - 1)
			grid[y, x:x+vec.shape[0]] = vec
		v += n - 1
		grid = np.rot90(grid)
	return _get_sides(grid, n - 2, maxval, v, x+1, y+1)

def make_goal(size):
	maxval = pow(size, 2) - 1
	grid = np.zeros((size, size), dtype=np.uint8)
	return _get_sides(grid, size, maxval)

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

class Solve(TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_xyz(self):
		pass

	
if __name__ == '__main__':
	if '-v' not in sys.argv:
		print(f'{bcolors.OKBLUE} Recommended usage: ./solvable.py -v {bcolors.ENDC}')
	ut.main()