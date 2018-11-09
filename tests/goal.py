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

from goal import get_goal_dict, make_goal

dir_path = dirname(realpath(__file__))
p_path = join(dir_path, "../n-puzzle.py")

def fold(grid, l, size, off=0):
	"""Utility to reshape a 1D array into spiral sq matrix"""
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
	"""Utility to reshape/reorder a spiral sq matrix to 1D array"""
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

class Goal(TestCase):
	def setUp(self):
		self.goals = {}
		for i in range (3, 10):
			self.goals[str(i)] = make_goal(i)

	def tearDown(self):
		pass

	def test_all_ints_in_range_on_board(self):
		all_ints_in_range = []
		for t in self.goals:
			tf = self.goals[t].flatten()
			all_ints_in_range.append(np.array_equal(np.sort(tf), np.arange(pow(int(t), 2), dtype=np.uint8)))
		self.assertNotIn(False, all_ints_in_range, msg='Not all ints are present on some.')

	def test_all_ints_contiguous(self):
		all_ints_contiguous = []
		for t in self.goals:
			tf = np.sort(self.goals[t].flatten())[1:]
			unfolded = np.array(unfold(self.goals[t], int(t)))[:-1]
			all_ints_contiguous.append(np.array_equal(tf, unfolded))
		self.assertNotIn(False, all_ints_contiguous, msg='Not all ints are contiguous.')

	
if __name__ == '__main__':
	if '-v' not in sys.argv:
		print(f'{bcolors.OKBLUE} Recommended usage: ./goal.py -v {bcolors.ENDC}')
	ut.main()