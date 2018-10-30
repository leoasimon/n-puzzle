import sys

def handle_error_none(msg):
	print(msg, file=sys.stderr)
	return None

def get_int_lst(l):
	return [int(e) for e in l]

def secured_open(filename):
	try:
		f = open(filename, 'r')
		return f
	except:
		return handle_error_none("No file {}".fornat(filename))

def checked(puzzle, size, options=[]):
	if len(puzzle) != size:
		return handle_error_none("Format error: size does not match")
	for row in puzzle:
		if len(row) != size:
			return handle_error_none("Format error: size does not match")
	return (puzzle, size, options)

def parsefile(name, options=[]):
	f = secured_open(name)
	if f == None:
		return None
	lines = [l[1].split() for l in enumerate(f) if l[1][0] != "#"]
	lines = [get_int_lst(l) for l in lines]
	size = int(lines.pop(0)[0])
	return checked(tuple([tuple(l) for l in lines]), size, options)

def parse():
	#try open file
	args = sys.argv[1:] if len(sys.argv) >= 2 else []
	options = [e.replace("-", "") for e in args if e[0] == '-']
	names = [e for e in args if e[0] != '-']
	if names:
		return parsefile(names[0], options)
	else:
		lines = [l.split() for l in sys.stdin if l[0] != "#"]
		size = int(lines.pop(0)[0])

		lines = [get_int_lst(l) for l in lines]
		return (tuple([tuple(l) for l in lines]), size, [])