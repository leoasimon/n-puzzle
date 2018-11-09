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
import numpy as np

from solvable import _get_inversions, get_solvable

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Valid(TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_solvable_if_side_len_odd_start_blank_odd(self):
		a = np.array([[8, 1, 3], [6, 2, 7], [0, 4, 5]])
		self.assertTrue(get_solvable(a, 3))

	def test_solvable_if_side_len_odd_start_blank_even(self):
		a = np.array([[2, 7, 8], [5, 0, 4], [3, 1, 6]])
		self.assertTrue(get_solvable(a, 3))

	def test_solvable_if_side_len_even_goal_blank_even(self):
		a = np.array([[2, 1, 11, 13], [10, 3, 9, 12], [5, 0, 4, 6], [7, 14, 8, 15]])
		self.assertTrue(get_solvable(a, 4))

	def test_solvable_if_side_len_even_goal_blank_odd(self):
		a = np.array([[3, 6, 15, 34, 35, 17], [16, 29, 23, 5, 20, 18], [10, 9, 22, 24, 14, 2], [27, 28, 1, 33, 4, 30], [32, 13, 8, 26, 31, 12], [0, 19, 25, 11, 7, 21]])
		self.assertTrue(get_solvable(a, 6))

	def test_solvable_sidelen_even_goalblank_odd_startblank_odd(self):
		a = np.array([[3, 6, 15, 34, 35, 17], [16, 29, 23, 5, 20, 18], [10, 9, 22, 24, 14, 2], [27, 28, 1, 33, 4, 30], [32, 13, 8, 26, 31, 12], [0, 19, 25, 11, 7, 21]])
		self.assertTrue(get_solvable(a, 6))

	def test_solvable_sidelen_even_goalblank_even_startblank_even(self):
		a = np.array([[7, 0, 8, 10], [3, 1, 2, 12], [14, 9, 5, 13], [4, 6, 11, 15]])
		self.assertTrue(get_solvable(a, 4))

class Unsolvable(TestCase):
	def test_unsolvable_sidelen_odd_start_odd(self):
		a = np.array([[6, 8, 2], [5, 3, 7], [0, 1, 4]])
		self.assertFalse(get_solvable(a, 3))

	def test_unsolvable_sidelen_odd_start_even(self):
		a = np.array([[8, 2, 1], [7, 0, 4], [6, 5, 3]])
		self.assertFalse(get_solvable(a, 3))

	def test_unsolvable_sidelen_even_start_odd_goal_even(self):
		a = np.array([[1, 14, 13, 6], [0, 12, 15, 2], [9, 11, 10, 8], [7, 3, 5, 4]])
		self.assertFalse(get_solvable(a, 4))

	def test_unsolvable_sidelen_even_start_even_goal_even(self):
		a = np.array([[9, 3, 7, 12], [1, 8, 15, 11], [10, 0, 5, 14], [13, 2, 6, 4]])
		self.assertFalse(get_solvable(a, 4))

	
if __name__ == '__main__':
	if '-v' not in sys.argv:
		print(f'{bcolors.OKBLUE} Recommended usage: ./solvable.py -v {bcolors.ENDC}')
	ut.main()