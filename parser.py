import sys

def get_int_lst(l):
	return [int(e) for e in l]

def parse():
	#try open file
	if len(sys.argv) >= 2:
		options = [e.replace("-", "") for e in sys.argv[1:] if e[0] == '-']
		name = [e for e in sys.argv[1:] if e[0] != '-'][0]
		with open(name, 'r') as f:
			lines = [l[1].split() for l in enumerate(f) if l[1][0] != "#"]
			lines = [get_int_lst(l) for l in lines]
			size = int(lines.pop(0)[0])
			return (tuple([tuple(l) for l in lines]), size, options)
	else:
		lines = [l.split() for l in sys.stdin if l[0] != "#"]
		size = int(lines.pop(0)[0])

		lines = [get_int_lst(l) for l in lines]
		return (tuple([tuple(l) for l in lines]), size, [])