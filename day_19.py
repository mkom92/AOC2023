import re
from math import prod
from util import timeit

def move_decode(move: str, part: dict):

	if len(move) <= 3:
		return move

	else:
		m = re.match(r'([a-z])(<|>)([0-9]+):([a-zA-Z]+)', move)
		if eval(f'{part[m.group(1)]} {m.group(2)} {m.group(3)}'):
			return m.group(4)

		else:
			return 'X'


def move_workflow(workflow: list, part: dict) -> list:

	follow_up_part = part.copy()
	follow_up_moves = []

	for check in workflow:

		if len(check) <= 3:
			follow_up_moves.append((check, follow_up_part))

		else:			

			m = re.match(r'([a-z])(<|>)([0-9]+):([a-zA-Z]+)', check)
			new_from, new_to = follow_up_part[m.group(1)]
			new_part = follow_up_part.copy()
			
			if m.group(2) == '<':

				new_part[m.group(1)] = (new_from, int(m.group(3))-1)
				follow_up_part[m.group(1)] = (int(m.group(3)), new_to)

			else:

				new_part[m.group(1)] = (int(m.group(3))+1, new_to)
				follow_up_part[m.group(1)] = (new_from, int(m.group(3)))

			follow_up_moves.append((m.group(4), new_part))

	return follow_up_moves


@timeit
def star(file_name: str, star_num: int) -> int:

	with open(file_name, 'r') as f:

		workflows = {}
		parts = []

		switch = False

		for line in f.readlines():

			if switch:

				items = [[j for j in i.split('=')] for i in line.strip()[1:-1].split(',')]

				p = {}
				for item in items:
					p[item[0]] = int(item[1])

				parts.append(p)

			else:

				if line == '\n':
					switch = True

				else:

					items = [i for i in line.strip().split('{')]

					workflows[items[0]] = [i for i in items[1][:-1].split(',')]


	if star_num == 1:

		accepted = 0

		for part in parts:

			outcome = 'X'
			current_workflow = 'in'

			while outcome == 'X':

				moves = workflows[current_workflow]

				for move in moves:
					current_outcome = move_decode(move, part)

					if current_outcome in ['A','R']:
						outcome = current_outcome
						break

					elif current_outcome == 'X':
						next

					else:
						current_workflow = current_outcome
						break

			if outcome == 'A':
				accepted += sum([value for key, value in part.items()])

	elif star_num == 2:

		accepted = 0
		part = {
			'x': (1,4000),
			'm': (1,4000),
			'a': (1,4000),
			's': (1,4000)
		}


		nodes = [('in', part)]

		while len(nodes) > 0:

			new_nodes = []

			for node in nodes:

				if len(node[0]) == 1:

					if node[0] == 'A':

						accepted += prod([v[1] - v[0] + 1 for k,v in node[1].items()])

				else:

					new_nodes += move_workflow(workflows[node[0]], node[1])

			nodes = new_nodes

	return accepted


if __name__ == '__main__':

	print(f"Star 1: {star('day_19.txt', 1)}")
	print(f"Star 2: {star('day_19.txt', 2)}")