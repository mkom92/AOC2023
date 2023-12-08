from re import match
from util import timeit
from math import gcd

def process_inp(file_name: str):

	with open(file_name, 'r') as f:

		inp_data = [j.strip() for j in f.readlines()]

	instruction = [1 if step == 'R' else 0 for step in inp_data[0]]

	nodes = {}

	for node_info in inp_data[2:]:
		m = match(r"(?P<node>[0-9A-Z]+) = \((?P<rl_nodes>[0-9A-Z]+\, [0-9A-Z]+)\)", node_info.strip())
		nodes[m.group('node')] = m.group('rl_nodes').split(', ')

	return instruction, nodes


@timeit
def star_1(file_name: str, from_node: str, to_nodes: list) -> int:

	instruction, nodes = process_inp(file_name)

	steps = 0

	curr_node = from_node
	curr_step = instruction[0]

	while curr_node not in to_nodes:

		steps += 1
		curr_node = nodes[curr_node][curr_step]
		curr_step = instruction[steps%len(instruction)]

	print(f"{from_node} - {curr_node}: {steps} steps")

	return steps

# @timeit
def star_2(file_name: str) -> int:

	instruction, nodes = process_inp(file_name)

	a_nodes, z_nodes = [i for i in nodes.keys() if i[-1] =='A'], [i for i in nodes.keys() if i[-1] =='Z']
	
	steps_az = []

	for a in a_nodes:

		steps_az.append(star_1(file_name, a, z_nodes))

	lcm = 1

	for i in steps_az:
		lcm = lcm*i//gcd(lcm, i)

	return lcm

if __name__ == "__main__":

	# print(f"Star 1: {star_1('day_8.txt','AAA','ZZZ')}")
	print(f"Star 2: {star_2('day_8.txt')}")
