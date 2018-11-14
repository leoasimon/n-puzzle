#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import deque

def get_path(curr_str, parents):
	l = []
	while curr_str is not None:
		l.append(curr_str)
		curr_str = parents[curr_str]
	return l

def print_solution(stats, n_str, parents, i):
	l = get_path(n_str, parents)

	print(f'Heuristic: {stats.heuristic}')
	print(f'Search type: {stats.algo}')
	print(f'Found solution in {stats.moves} moves.')
	print(f'Total number added to open set (time complexity):  {stats.total_open}')
	print(
		f'Max nodes in memory (space complexity):  {stats.max_open} '
		f'(plus {len(parents) * 3})' # For g_score, f_score, and parents dicts
	) #TODO: DB?

	return l