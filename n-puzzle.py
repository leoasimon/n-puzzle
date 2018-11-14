#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

import cProfile

from parsing import parse
from a_star import solve
from create_db import get_db

def get_dbs(s):
	return [get_db(size, name) for name in ['a', 'b', 'c']]

if __name__ == '__main__':
	a, size, options = parse()
	dbs = get_dbs(size) if options.heuristic == 'db' else []
	solve(a, size, options, dbs)
	sys.exit(0)
	