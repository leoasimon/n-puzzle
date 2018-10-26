#! /usr/bin/env python3

import sys
import re

import cProfile

from parser import parse
from a_star import solve

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
	import queue as Q

if __name__ == '__main__':
	a, size = parse()
	solve(a, size)