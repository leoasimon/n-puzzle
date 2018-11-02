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

from heuristics import get_manhattan
from goal import get_goal_dict, make_goal

dir_path = dirname(realpath(__file__))
p_path = join(dir_path, "../n-puzzle.py")
print(p_path)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Manhattan(TestCase):
	def setUp(self):
		self.size = 3
		self.goal = make_goal(self.size)
		self.goal_dict = get_goal_dict(self.goal, self.size)

	def tearDown(self):
		pass

	def test_manhattan_solved_is_0(self):
		f_solved = join(getcwd(), "puzzles/valids/solved_3x3")
		solved_grid, _, _ = parsefile(f_solved)
		h = get_manhattan(solved_grid, self.goal, self.goal_dict, self.size)
		self.assertEqual(0, h)

	def test_manhattan_easiest_is_1(self):
		f_easy = join(getcwd(), "puzzles/valids/easiest_3x3.1")
		easy_grid, _, _ = parsefile(f_easy)
		h = get_manhattan(easy_grid, self.goal, self.goal_dict, self.size)
		self.assertEqual(1, h)

	def test_manhattan_hardest_equals_24(self):
		f = join(getcwd(), "puzzles/valids/hardest_3x3")
		grid, _, _ = parsefile(f)
		h = get_manhattan(grid, self.goal, self.goal_dict, self.size)
		self.assertEqual(24, h, f'{bcolors.FAIL} wrong h score for hardest_3x3 {bcolors.ENDC}')
	
if __name__ == '__main__':
	if '-v' not in sys.argv:
		print(f'{bcolors.OKBLUE} Recommended usage: ./heuristics.py -v {bcolors.ENDC}')
	ut.main()