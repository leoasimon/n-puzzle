#! /usr/bin/env python3

from os import getcwd, listdir
from os.path import join, dirname, realpath
import sys
from unittest import TestCase
import unittest as ut
import numpy as np
sys.path.insert(0, join(getcwd(), "../"))

from bfs import build_key

dir_path = dirname(realpath(__file__))
p_path = join(dir_path, "../n-puzzle.py")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class BuildKey(TestCase):
	def setUp(self):
		self.size = 4
		self.goal = np.array([
			[1,-1,-1,-1],
			[12,13,-1,-1],
			[11,-1,-1,-1],
			[10,9,-1,-1],
		])
		self.nums = [e for e in self.goal.flatten() if e != -1]

	def test_base_key(self):
		key = build_key(self.goal, self.nums)
		self.assertEqual("000111020313", key)

	def test_one_swap(self):
		swaped = np.array([
			[1,-1,-1,-1],
			[12,-1,-1,-1],
			[11,-1,-1,-1],
			[10,9,-1,-1],
		])
		key = build_key(swaped, self.nums)
		self.assertEqual("0001-1-1020313", key)

	def test_none_here(self):
		swaped = np.array([
			[-1,-1,-1,-1],
			[-1,-1,-1,-1],
			[-1,-1,-1,-1],
			[-1,-1,-1,-1],
		])
		key = build_key(swaped, self.nums)
		self.assertEqual("-1-1-1-1-1-1-1-1-1-1-1-1", key)

if __name__ == '__main__':
	if '-v' not in sys.argv:
		print(f'{bcolors.OKBLUE} Recommended usage: ./heuristics.py -v {bcolors.ENDC}')
	ut.main()