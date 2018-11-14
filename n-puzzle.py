#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

import cProfile

from parsing import parse
from a_star import solve

if __name__ == '__main__':
	a, size, options = parse()
	solve(a, size, options)
	sys.exit(0)