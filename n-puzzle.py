#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from parsing import parse
from a_star import solve

if __name__ == '__main__':
	start, size, options = parse()
	solve(start, size, options)
	sys.exit(0)