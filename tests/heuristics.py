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
from parsing import parsefile
import numpy as np

from heuristics import get_manhattan, get_linear_conflicts, get_misplaced_tiles
from goal import get_goal_dict, make_goal

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

class LinearC(TestCase):
	def setUp(self):
		self.size = 3
		self.goal = make_goal(self.size)
		self.goal_dict = get_goal_dict(self.goal, self.size)
	
	def test_linear_conflicts_row(self):
		g = np.array([[3,1,2],[8,0,4],[7,6,5]])
		lc = get_linear_conflicts(g, self.goal, self.goal_dict, self.size)
		self.assertEqual(2, lc, f'{bcolors.FAIL} wrong lc score {bcolors.ENDC}')
	
	def test_linear_conflicts_col(self):
		g = np.array([[8,2,3],[1,0,4],[7,6,5]])
		lc = get_linear_conflicts(g, self.goal, self.goal_dict, self.size)
		self.assertEqual(2, lc, f'{bcolors.FAIL} wrong lc score {bcolors.ENDC}')
	
	def test_linear_conflicts_row_tricky(self):
		g = np.array([[3,2,1],[8,0,4],[7,6,5]])
		lc = get_linear_conflicts(g, self.goal, self.goal_dict, self.size)
		self.assertEqual(4, lc, f'{bcolors.FAIL} wrong lc score {bcolors.ENDC}')
	
	def test_linear_conflicts_col_tricky(self):
		g = np.array([[7,2,3],[8,0,4],[1,6,5]])
		lc = get_linear_conflicts(g, self.goal, self.goal_dict, self.size)
		self.assertEqual(4, lc, f'{bcolors.FAIL} wrong lc score {bcolors.ENDC}')
	
	def test_linear_conflicts_col_and_row(self):
		g = np.array([[7,2,3],[8,0,4],[1,5,6]])
		lc = get_linear_conflicts(g, self.goal, self.goal_dict, self.size)
		self.assertEqual(6, lc, f'{bcolors.FAIL} wrong lc score {bcolors.ENDC}')

class MisplacedT(TestCase):
	def setUp(self):
		self.size = 4
		self.goal = make_goal(self.size)
	
	def test_misplaced_all_good(self):
		g = self.goal
		mt = get_misplaced_tiles(g, self.goal)
		self.assertEqual(0, mt, f'{bcolors.FAIL} wrong mt score {bcolors.ENDC}')
	
	def test_misplaced_all_messed(self):
		g = np.array([
			[15,14,13,12],
			[4,3,2,11],
			[5,0,1,10],
			[6,8,7,9],
		])
		mt = get_misplaced_tiles(g, self.goal)
		self.assertEqual(15, mt, f'{bcolors.FAIL} wrong mt score {bcolors.ENDC}')
	
	def test_misplaced_two(self):
		g = np.array([
			[1,2,3,4],
			[12,13,14,5],
			[11,9,15,6],
			[10,0,8,7],
		])
		mt = get_misplaced_tiles(g, self.goal)
		self.assertEqual(1, mt, f'{bcolors.FAIL} wrong mt score {bcolors.ENDC}')
	
	def test_misplaced_five(self):
		g = np.array([
			[3,2,1,4],
			[12,13,14,5],
			[11,9,15,7],
			[10,0,8,6],
		])
		mt = get_misplaced_tiles(g, self.goal)
		self.assertEqual(5, mt, f'{bcolors.FAIL} wrong mt score {bcolors.ENDC}')


if __name__ == '__main__':
	if '-v' not in sys.argv:
		print(f'{bcolors.OKBLUE} Recommended usage: ./heuristics.py -v {bcolors.ENDC}')
	ut.main()