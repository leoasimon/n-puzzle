import sys

def print_grid(grid):
	for line in grid:
		print(line)

def print_scores(o, f_scores):
	for e in o:
		print("score: {}".format(f_scores[e]))

#Todo: move it in a more relevant file
def get_path(curr, parents, moves):
	if curr == None:
		return []
	l = get_path(parents[curr], parents, moves + 1)
	l.append(curr)
	return l

def print_solution(n, parents, i):
	l = get_path(n, parents, 0)
	for j, e in enumerate(l):
		print(f'move: {j}', end=' ')
		print(e)
	sys.exit(0)