#! /usr/bin/env python3

import sys
import re
from parser import parse
from a_star import solve

if __name__ == '__main__':
	a, size = parse()
	solve(a, size)