import sys

def print_grid(grid):
	for line in grid:
		print(line)

def print_scores(o, f_scores):
	for e in o:
		print("score: {}".format(f_scores[e]))

def get_path(curr, parents, moves):
	if curr == None:
		print("end!")
		return
	get_path(parents[curr], parents, moves + 1)
	print("Move #{}: {}".format(moves, parents[curr]))

def print_solution(n, parents, i):
    print("Got to goal after " + str(i) + " searches.")
    get_path(parents[n], parents, 0)
    sys.exit(0)