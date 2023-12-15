import re
from util import timeit

def hash(inp: str) -> int:

	val = 0

	for t in inp:
		val = ((val+ord(t))*17)%256

	return val

@timeit
def star_1(file_name: str) -> int:

	with open(file_name,'r') as f:
		inp = [val.strip() for val in f.read().split(',')]

	total_val = 0
	for i in inp:
		total_val += hash(i)


	return total_val

@timeit
def star_2(file_name: str) -> int:

	with open(file_name,'r') as f:
		inp = [val.strip() for val in f.read().split(',')]


	boxes = {i: [] for i in range(256)}
	labels = {}

	for lense in inp:

		sign_pos = re.search(r'(=|-)', lense)
		label = lense[:sign_pos.start()]
		sign =	lense[sign_pos.start()]
		box = hash(label)

		if sign == '=':
			labels[label] = int(lense[sign_pos.start()+1:])
			if label not in boxes[box]:
				boxes[box].append(label)
		elif sign == '-':
			labels[label] = None
			try:
				boxes[box].remove(label)
			except:
				next

	total_val = 0
	for box, b_labels in boxes.items():

		total_val += sum([(box + 1) * (n + 1) * labels[l] for n,l in enumerate(b_labels)])

	return total_val


if __name__ == '__main__':
	print(f"Star 1: {star_1('day_15.txt')}")
	print(f"Star 2: {star_2('day_15.txt')}")