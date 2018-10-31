#! /usr/bin/env python3

import sys
import re

import cProfile

from parser import parse
from a_star import solve
from gui import display_all

if __name__ == '__main__':
	a, size, options = parse()
	path = solve(a, size)
	# for j, e in enumerate(path):
	# 	print(f'move: {j}', end=' ')
	# 	print(e)
	if "g" in options:
		display_all(size, path)
	sys.exit(0)
	