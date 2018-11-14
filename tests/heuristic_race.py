#! /usr/bin/env python3

from os import getcwd
from os.path import join, dirname, realpath
import sys
import subprocess
from unittest import TestCase
import unittest as ut
import time
from io import StringIO

sys.path.insert(0, join(getcwd(), "../"))
from parsing import parse_stdin

dir_path = dirname(realpath(__file__))
p_path = join(dir_path, "../n-puzzle.py")
g_path = join(dir_path, "../puzzle_generator.py")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

class Race(TestCase):
	def setUp(self):
		self.n_3x3 = 10
		self.n_4x4 = 1
		self.labels = {
			"mh": "Manhattan distance",
			"mt": "Misplaced tiles",
			"lc": "Manhattan distance + linear conflict",
			"db": "Pattern database",
		}
		self.times = {
			"mh": 0,
			"mt": 0,
			"lc": 0,
			"db": 0
		}

	def test_race_3x3(self):
		print(bcolors.HEADER + "-----RACE 3x3-----")
		heuristics = ["mh", "mt", "lc"]
		print(bcolors.OKGREEN)
		for i in range(self.n_3x3):
			progress(i, self.n_3x3)
			for h in heuristics:
				with  subprocess.Popen(["python", g_path, "3", "-s"], stdout=subprocess.PIPE) as ps:
					s = time.time()
					out = subprocess.check_output([p_path, "-he", h], stdin=ps.stdout)
					self.times[h] += time.time() - s
		print(bcolors.OKBLUE)
		print(f'result for {self.n_3x3} generated puzzles:\n')
		for h in heuristics:
			print(f'{self.labels[h]}: {self.times[h]}s')
	
if __name__ == '__main__':
	ut.main()
