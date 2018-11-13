#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def get_path(curr_str, parents, moves):
	if curr_str is None:
		return []
	l = get_path(parents[curr_str], parents, moves + 1)
	l.append(curr_str)
	return l

def print_solution(stats, n_str, parents, i):
	l = get_path(n_str, parents, 0)
	# TODO: Format
	print(f'Heuristic: {stats.heuristic}')
	print(f'Search type: {stats.algo}')
	print(f'Found solution in {stats.moves} moves.')
	print(f'Total number added to open set (time complexity):  {stats.total_open}')
	print(f'Max nodes in memory (space complexity):  {stats.max_open}') #TODO: Consider DB, dicts, etc?

	#TODO: Print path
	return l