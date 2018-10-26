import sys

def get_int_lst(l):
	return [int(e) for e in l]

def parse():
	lines = [l.split() for l in sys.stdin if l[0] != "#"]
	size = int(lines.pop(0)[0])

	lines = [get_int_lst(l) for l in lines]
	return (tuple([tuple(l) for l in lines]), size)