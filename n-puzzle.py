#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

import cProfile

from parsing import parse
from a_star import solve
# from gui import display_all

if __name__ == '__main__':
	a, size, options = parse()
	path = solve(a, size, options)
	# for j, e in enumerate(path):
	# 	print(f'move: {j}', end=' ')
	# 	print(e)
	# if "g" in options:
	# 	display_all(size, path)
	sys.exit(0)
	