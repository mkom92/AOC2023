import re
from sympy.utilities.iterables import multiset_permutations
from json import dumps

def star(file_name: str, star_num: int) -> int:

	with open(file_name, 'r') as f:
		parts_records = {}

		p_damaged  = re.compile("\#+")
		p_unknown  = re.compile("\?")

		for n,line in enumerate(f.readlines()):

			newline = [i for i in line.strip().split()]
			parts_records[n] = {}
			parts_records[n]['instruction'] = newline[0]
			parts_records[n]['instruction_next'] = newline[0]+ '?' + newline[0]
			parts_records[n]['parts_map'] = [int(i) for i in newline[1].split(',')]
			# parts_records[n]['damaged_pos'] = [(m.start(), m.start() + len(m.group()) - 1) for m in p_damaged.finditer(newline[0])]
			parts_records[n]['unknown_pos'] = [int(m.start()) for m in p_unknown.finditer(newline[0])]
			parts_records[n]['unknown_pos_next'] = [int(m.start()) for m in p_unknown.finditer(newline[0]+'?'+newline[0])]

	total_ct, total_ct_next = 0,0
	for n, line in parts_records.items():

		unknowns = len(line['unknown_pos'])
		damaged =  sum([len(m.group()) for m in p_damaged.finditer(line['instruction'])])
		max_damaged = sum(line['parts_map'])

		inp_string = '#'*(max_damaged-damaged) + '.'*(unknowns-(max_damaged-damaged))
		sub_ct = 0

		for i in multiset_permutations(inp_string):
			new_line = line['instruction']
			for m,pos in enumerate(line['unknown_pos']):

				new_line = new_line[:pos] + i[m] + new_line[pos+1:]

			if [len(m.group()) for m in p_damaged.finditer(new_line)] == line['parts_map']:
				sub_ct += 1

		parts_records[n]['match_ct'] = sub_ct
		total_ct += sub_ct

		unknowns_next = len(line['unknown_pos_next'])
		inp_string_next = '#'*(max_damaged-damaged)*2 + '.'*(unknowns_next-((max_damaged-damaged)*2))
		sub_ct_next = 0

		for i in multiset_permutations(inp_string_next):
			new_line = line['instruction_next']
			for m,pos in enumerate(line['unknown_pos_next']):

				new_line = new_line[:pos] + i[m] + new_line[pos+1:]

			if [len(m.group()) for m in p_damaged.finditer(new_line)] == line['parts_map']*2:
				sub_ct_next += 1

		parts_records[n]['match_ct_next'] = sub_ct_next
		total_ct_next += (sub_ct_next/sub_ct)**4 * sub_ct

		sub_ct = 0
		sub_ct_next = 0


	# print(dumps(parts_records, indent=4))
	if star_num == 1:
		return total_ct 
	elif star_num == 2:
		return total_ct_next

if __name__ == "__main__":
	print(f"Star 1: {star('day_12.txt',1)}")
	# print(f"Star 2: {star('day_12.txt',2)}")