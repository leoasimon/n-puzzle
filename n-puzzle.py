#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

import cProfile

from parsing import parse
from a_star import solve
from gui import display_all
from create_db import get_db

def get_dbs(s):
	return [get_db(size, name) for name in ['a', 'b', 'c']]

if __name__ == '__main__':
	print(f'Using interpreter : {sys.executable}')
	a, size, options = parse()
	dbs = get_dbs(size) if "db" in options else []
	path = solve(a, size, options, dbs)
	# for j, e in enumerate(path):
	# 	print(f'move: {j}', end=' ')
	# 	print(e)
	if "g" in options:
		display_all(size, path)
	sys.exit(0)
	