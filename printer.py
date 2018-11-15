#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import deque

from gui import display_all

class C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def _get_path(curr_str, parents):
	l = []
	while curr_str is not None:
		l.append(curr_str)
		curr_str = parents[curr_str]
	return list(reversed(l))

def print_solution(stats, n_str, parents, options={}):
	if options.verbose or options.gui:
		path = _get_path(n_str, parents)

		if options.verbose:
			for j, e in enumerate(path):
				print(f'move: {j}', end=' ')
				print(e)

	print(f'\n--- Found solution in {C.HEADER}{stats.moves}{C.ENDC} moves. ---\n')
	print(f'Heuristic:                                         {C.BOLD}{stats.h_name}{C.ENDC}')
	print(f'Search type:                                       {C.BOLD}{stats.algo}{C.ENDC}')
	print(f'Time complexity:'
		f'\n\tTotal added to open queue: {C.BOLD}{stats.total_open}{C.ENDC}')
	print(
		f'Space complexity:'
		f'\n\tOpen set max:              {C.BOLD}{stats.max_open}{C.ENDC}'
		f'\n\tLookup dicts:              {C.BOLD}3 * {len(parents)}{C.ENDC}' # For g_score, f_score, and parents dicts
	)
	if options.heuristic == 'db':
		print(
		f'\tPattern database:          {3360 + 5765760 + 5765760}')
	
	if options.gui:
		display_all(stats.size, path)