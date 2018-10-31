import numpy as np
import scipy.spatial.distance

def get_manhattan(grid, goal, goal_dict, size):
	diff = 0
	# TODO: Try iterators instead...? I tried this, but it doesn't seem faster	
	# it = np.nditer(grid, flags=['multi_index'])
	# while not it.finished:
	# 	goal_pos_x, goal_pos_y = goal_dict[str(it[0])]
	# 	diff += abs(it.multi_index[0] - goal_pos_y) + abs(it.multi_index[1] - goal_pos_x)
	# 	it.iternext()

	# Without iterators:
	for y in range(size):
		for x, val in enumerate(grid[y]):
			if val:
				goal_pos_x, goal_pos_y = goal_dict[str(val)]
				diff += abs(x - goal_pos_x) + abs(y - goal_pos_y)
	return diff

def get_h_score(grid, goal, goal_dict, size):
	# Todo: chose one heuristic, default manhattan
	return get_manhattan(grid, goal, goal_dict, size)