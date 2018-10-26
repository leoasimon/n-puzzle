#! /usr/bin/env python3

import sys
import re

import cProfile

from parser import parse
from a_star import solve

if __name__ == '__main__':
	a, size = parse()
	path = solve(a, size)
	for n in path:
		print(n)