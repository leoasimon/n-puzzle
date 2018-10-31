import sys

def print_grid(grid):
	for line in grid:
		print(line)

def print_scores(o, f_scores):
	for e in o:
		print("score: {}".format(f_scores[e]))

#Todo: move it in a more relevant file
def get_path(curr_str, parents, moves):
	if curr_str is None:
		return []
	l = get_path(parents[curr_str], parents, moves + 1)
	l.append(curr_str)
	return l

def print_solution(n_str, parents, i):
	l = get_path(n_str, parents, 0)
	return l