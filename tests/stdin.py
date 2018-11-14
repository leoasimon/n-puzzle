#! /usr/bin/env python3

from os import getcwd, listdir
from os.path import join, dirname, realpath
import sys
import subprocess
from unittest import TestCase
import unittest as ut

sys.path.insert(0, join(getcwd(), "../"))
from parsing import parse_stdin

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

dir_path = dirname(realpath(__file__))
p_path = join(dir_path, "../n-puzzle.py")

class Stdin(TestCase):
	def tearDown(self):
		pass

	def test_invalid(self):
		print(bcolors.HEADER + "-----INVALID STDIN-----")
		files = listdir(join(getcwd(), "puzzles/invalids"))
		errors = []
		for fname in files:
			print(bcolors.OKBLUE + fname + bcolors.ENDC)
			path = join(getcwd(), "puzzles/invalids", fname)
			with  subprocess.Popen(('cat', path), stdout=subprocess.PIPE) as ps:
				try:
					out = subprocess.check_output((p_path), stdin=ps.stdout, shell=True, 
					timeout=3, universal_newlines=True)
				except:
					errors.append(fname)
		self.assertCountEqual(files, errors)

	def test_valids(self):
		print(bcolors.HEADER + "-----VALIDS STDIN-----")
		files = listdir(join(getcwd(), "puzzles/valids"))
		errors = []
		for fname in files:
			print(bcolors.OKBLUE + fname + bcolors.ENDC)
			path = join(getcwd(), "puzzles/valids", fname)
			with  subprocess.Popen(('cat', path), stdout=subprocess.PIPE) as ps:
				try:
					out = subprocess.check_output((p_path), stdin=ps.stdout, shell=True, 
					timeout=3, universal_newlines=True)
					print(out)
				except:
					errors.append(fname)
	
if __name__ == '__main__':
	ut.main()
