#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# 
import sys
import numpy as np
from solvable import get_solvable
import argparse

class PuzzleProblem(Exception):
	pass

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

# return: tuple(2D array, int, options[])
def checked(puzzle, size, options={}):
	if size > 10:
		raise PuzzleProblem("That puzzle is too big for me.")
	if not all(len(y) == len(puzzle) == size for y in puzzle):
		raise PuzzleProblem("Format error: size does not match.")
	if not (np.array_equal(np.sort(puzzle.flatten()), np.arange(pow(size, 2), dtype=np.uint8))):
		raise PuzzleProblem("Puzzle error: Invalid numeric range in puzzles.")
	if not get_solvable(puzzle, size):
		raise PuzzleProblem("Puzzle error: Unsolvable puzzle.")
	return (puzzle, size, options)

# params: filename
# return tuple(int, 2D array)
def file_to_lines(fd):
	try:
		usable_lines = [line.rstrip('\n').split() for line in fd if '#' not in line]
		int_lines = [get_int_lst(l) for l in usable_lines]
		size = int_lines[0][0]
		puzzle = int_lines[1:]
		return (size, puzzle)
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

# params: filename, options[]
# return tuple(2D array, int, [options])
def parsefile(name, options={}):
	f = secured_open(name)
	size, puzzle = file_to_lines(f)
	f.close()
	return checked(np.array(puzzle, dtype=np.uint8), size, options)
	
def parse_stdin(options={}):
	size, puzzle = stdin_to_line()
	return checked(np.array(puzzle, dtype=np.uint8), size, options)

# return tuple(2D array, int, [options])
def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument("name", nargs="?", help="Name of the file to open")
	parser.add_argument("-g", "--gui", action="store_true", help="Display the solution in a gui window")
	parser.add_argument("-v", "--verbose", action="store_true", help="Display the different states of the solution")

	heuristics = ["lc","mh","db","mt"]
	parser.add_argument("-he", "--heuristic", default="mh", choices=heuristics, help="choose a heuristic function")

	parser.add_argument("-a", "--algorithm", default="astar", choices=["astar", "greedy"])

	args = parser.parse_args()

	if args.name:
		try:
			return parsefile(args.name, args)
		except PuzzleProblem as pp:
			sys.exit(f'\033[91m{str(pp)}\033[0m')
	else:
		try:
			return parse_stdin(args)
		except PuzzleProblem as pp:
			sys.exit(f'\033[91m{str(pp)}\033[0m')