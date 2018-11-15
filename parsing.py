#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import numpy as np

from error import PuzzleProblem
from solvable import get_solvable, generate_solvable
from printer import C

def get_int_lst(l):
	try:
		return [int(e) for e in l]
	except TypeError:
		raise PuzzleProblem("Format error: Non-numeric input where integer expected.")
	except ValueError:
		raise PuzzleProblem("Format error: Problematic numeric value.")

def secured_open(filename):
	try:
		f = open(filename, 'r')
		return f
	except:
		raise PuzzleProblem(f'No file {filename}')

def checked(lines, size, options={}):
	if not lines or not size:
		raise PuzzleProblem("Missing size or puzzle data.")
	elif len(lines) != size:
		raise PuzzleProblem("Puzzle length does not match size.")
	elif size < 3:
		raise PuzzleProblem("That puzzle is too small.")
	elif size > 15:
		raise PuzzleProblem("That puzzle is too big for me.")

	if not all(len(y) == len(lines) == size for y in lines):
		raise PuzzleProblem("Format error: puzzle is not a square.")

	lines_flattened = np.array([j for line in lines for j in line])
	if not (np.array_equal(np.sort(lines_flattened), np.arange(size ** 2, dtype=np.uint8))):
		raise PuzzleProblem("Puzzle error: Invalid numeric range in puzzles.")

	puzzle = np.reshape(lines_flattened, (size, size))
	if not get_solvable(puzzle, size):
		raise PuzzleProblem("Puzzle error: Unsolvable puzzle.")
	return (puzzle, size, options)

def file_to_lines(fd):
	try:
		usable_lines = [line.rstrip('\n').split() for line in fd if '#' not in line]
		int_lines = [get_int_lst(l) for l in usable_lines]
		size = int_lines[0][0]
		puzzle_lines = int_lines[1:]
		return (size, puzzle_lines)
	except IndexError:
		raise PuzzleProblem("Format error: Problem with input file lines.")
	except UnicodeDecodeError:
		raise PuzzleProblem("Format error: File type is not valid")

def stdin_to_line():
	try:
		lines = [l.split() for l in sys.stdin if l[0] != "#"]
		size = int(lines.pop(0)[0])
		lines = [get_int_lst(l) for l in lines]
		return (size, lines)
	except IndexError:
		raise PuzzleProblem("Format error: Problem with input file lines.")
	except UnicodeDecodeError:
		raise PuzzleProblem("Format error: File type is not valid")
	except ValueError:
		raise PuzzleProblem("Format error: Problematic numeric value.")
	except TypeError:
		raise PuzzleProblem("Format error: Non-numeric input where integer expected.")

def parsefile(name, options={}):
	f = secured_open(name)
	size, lines = file_to_lines(f)
	f.close()
	return checked(lines, size, options)
	
def parse_stdin(options={}):
	size, lines = stdin_to_line()
	return checked(lines, size, options)

# return tuple(2D array, int, args)
def parse():
	heuristics = ["lc","mh","db","mt"]
	algorithm_types = ["astar", "greedy", "uniform"]
	parser = argparse.ArgumentParser()

	parser.add_argument("name", nargs="?", help="Name of the file to open")
	parser.add_argument("-rp", "--randompuzzle", type=int, help="Create a random solvable puzzle with edge length of given size")
	parser.add_argument("-g", "--gui", action="store_true", help="Display the solution in a gui window")
	parser.add_argument("-v", "--verbose", action="store_true", help="Display the different states of the solution")
	parser.add_argument("-he", "--heuristic", default="mh", choices=heuristics, help="choose a heuristic function")
	parser.add_argument("-a", "--algorithm", default="astar", choices=algorithm_types)

	args = parser.parse_args()

	try:
		if args.randompuzzle:
			size = args.randompuzzle
			return (generate_solvable(size), size, args)
		elif args.name:
			return parsefile(args.name, args)
		else:
			return parse_stdin(args)
	except PuzzleProblem as pp:
		sys.exit(f'{C.FAIL}{str(pp)}{C.ENDC}')