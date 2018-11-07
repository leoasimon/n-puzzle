#! /usr/bin/env python3

from io import StringIO
from os import getcwd, listdir
from os.path import join, dirname, realpath
import sys
import subprocess
from unittest import TestCase, TestSuite, TextTestRunner
from unittest.mock import patch
sys.path.insert(0, join(getcwd(), "../"))
from parsing import parsefile, PuzzleProblem

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

class Parser(TestCase):
	def test_invalid(self):
		print(bcolors.HEADER + "-----INVALID FILES-----")
		files = listdir(join(getcwd(), "puzzles/invalids"))
		errs = []
		for i, fname in enumerate(files):
			print(bcolors.OKBLUE + fname + bcolors.ENDC)
			path = join(getcwd(), "puzzles/invalids", fname)
			try:
				parsefile(path)
			except PuzzleProblem:
				errs.append(fname)
		self.assertCountEqual(errs, files)

class Large(TestCase):
	def test_large(self):
		print(bcolors.HEADER + "-----LARGE FILES-----")
		files = listdir(join(getcwd(), "puzzles/large"))
		for fname in files:
			print(bcolors.OKBLUE + fname)
			path = join(getcwd(), "puzzles/large", fname)
			try:
				out1 = subprocess.check_output([p_path, path], timeout=1)
				print(out1.decode())
			except subprocess.TimeoutExpired as e:
				print(f'{bcolors.FAIL} {str(e)} {bcolors.ENDC} \n')
	def test(self):
		self.test_large()

class Main(TestCase):
	def test_main(self):
		print(bcolors.HEADER + "-----VALIDS-----")
		files = listdir(join(getcwd(), "puzzles/valids"))
		for fname in files:
			print(bcolors.OKBLUE + fname)
			path = join(getcwd(), "puzzles/valids", fname)
			out1 = subprocess.check_output([p_path, path])
			print(out1.decode())
	def test(self):
		self.test_main()

if __name__ == "__main__":
	allargs = ["parser", "main", "large"]
	args = [e for e in sys.argv if e in allargs]
	args = allargs if len(args) == 0 else args

	if "parser" in args:
		suite = TestSuite()
		suite.addTest(Parser('test_invalid'))
		runner = TextTestRunner()
		runner.run(suite)

	if "large" in args:
		large = Large()
		large.test()
	
	if "main" in args:
		main = Main()
		main.test()