#! /usr/bin/env python3

import sys
import re

import cProfile

from parser import parse
from a_star import solve
from gui import display_all

if __name__ == '__main__':
	a, size = parse()
	path = solve(a, size)
	for n in path:
		print(n)
	# Todo: create -g option for gui mode
	# display_all(size, path)