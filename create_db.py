#! /usr/bin/env python3
# 
import numpy as np
import json
from bfs import bfs
import sys
import os

def handle_error(msg):
	print(msg, file=sys.stderr)
	sys.exit(1)

def save_json(db, s, n):
	name = f'{s}x{s}_{n}.json'
	with open(name, "w") as f:
		jf = json.dumps(db)
		f.write(jf)

def get_db(s, n):
	name = f'{s}x{s}_{n}.json'
	path = os.path.join(os.path.abspath("dbs"), name)
	try:
		f = open(path, "r")
		d = json.load(f)
		f.close()
		return d
	except:
		handle_error(f'No database available for {s*s - 1} puzzles')

def get_goals(s):
	with open("goals.json", "r") as f:
		g_dict = json.load(f)
		names = [f'{s}x{s}_a', f'{s}x{s}_b', f'{s}x{s}_c']
		g_list = [np.array(e) for e in [g_dict[n] for n in names]]
		return g_list

# def get_goals(size):
# 	#Todo: handle different sizes
# 	a = np.array([
# 		[1,2,3],
# 		[-1,-1,-1],
# 		[-1,-1,-1]
# 	])
# 	b = np.array([
# 		[-1,-1,-1],
# 		[8,-1,4],
# 		[-1,-1,-1]
# 	])
# 	c = np.array([
# 		[-1,-1,-1],
# 		[-1,-1,-1],
# 		[7,6,5]
# 	])
# 	return [a,b,c]


def createDb():
	args = sys.argv[1:] if len(sys.argv) >= 2 else []
	size = 3 if not args else int(args[0])
	print(size)
	goals = get_goals(size)
	for g, name in zip(goals, ['a', 'b', 'c']):
		db = bfs(g, size, (1,1))
		save_json(db, size, name)

if __name__ == "__main__":
	createDb()