def get_manhattan(grid, goal_dict, size): # TODO: Haven't tested
	diff = 0
	for y in range(size):
		for x in range(size):
			grid_val = grid[y][x]
			goal_pos_x, goal_pos_y = goal_dict[str(grid_val)]
			distance_x = abs(x - goal_pos_x)
			distance_y = abs(y - goal_pos_y)
			diff += distance_x + distance_y
	return diff

def get_h_score(grid, goal_dict, size):
	# Todo: chose one heuristic, default manhattan
	return get_manhattan(grid, goal_dict, size)