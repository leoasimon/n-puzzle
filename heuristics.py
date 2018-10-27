import numpy as nm
import scipy.spatial.distance

def get_manhattan(grid, goal, goal_dict, size): # TODO: Haven't tested
	diff = 0
	for y in range(size):
		for x, val in enumerate(grid[y]):
			if val:
				goal_pos_x, goal_pos_y = goal_dict[str(val)]
				diff += abs(x - goal_pos_x) + abs(y - goal_pos_y)
	return diff

def get_h_score(grid, goal, goal_dict, size):
	# Todo: chose one heuristic, default manhattan
	return get_manhattan(grid, goal, goal_dict, size)


# def get_manhattan_2(prev_h, val, old_pos, new_pos, goal, goal_dict, size):
# 	goal_pos_x, goal_pos_y = goal_dict[val]
# 	old_pos_x, old_pos_y = goal_dict[val]
# 	new_pos_x, new_pos_y = new_pos
# 	prev_h -= abs(old_pos_x - goal_pos_x) + abs(old_pos_y - goal_pos_y)
# 	h = prev_h + abs(new_pos_x - goal_pos_x) + abs(new_pos_y - goal_pos_y)
# 	return h


# def get_h_score_2(prev_h, val, old_pos, new_pos, goal, goal_dict, size):
# 	return get_manhattan_2(prev_h, val, old_pos, new_pos, goal, goal_dict, size)