#! /usr/bin/env python3
# 
import numpy as np
import json
from bfs import bfs

def save_json(db, s, n):
	name = f'{s}x{s}_{n}.json'
	with open(name, "w") as f:
		jf = json.dumps(db)
		f.write(jf)

def get_db(s, n):
	name = f'{s}x{s}_{n}.json'
	with open(name, "r") as f:
		return json.load(f)



def get_goals(size):
	#Todo: handle different sizes
	a = np.array([
		[1,2,3],
		[-1,-1,-1],
		[-1,-1,-1]
	])
	b = np.array([
		[-1,-1,-1],
		[8,0,4],
		[-1,-1,-1]
	])
	c = np.array([
		[-1,-1,-1],
		[-1,-1,-1],
		[7,6,5]
	])
	return [a,b,c]


def createDb():
	size = 3
	goals = get_goals(size)
	for g, name in zip(goals, ['a', 'b', 'c']):
		db = bfs(g, size, (1,1))
		save_json(db, size, name)

if __name__ == "__main__":
	createDb()