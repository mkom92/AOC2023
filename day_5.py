import pandas as pd 
from util import timeit

def create_df(data_inp):

	data = {
	'source_start': []
	,'source_end': []
	,'destination_start': []
	,'destination_end': []
	,'range_length': []
	}

	for row in data_inp.split('\n')[1:]:

		row_split = [int(i) for i in row.split()]
		data['source_start'].append(row_split[1])
		data['source_end'].append(row_split[1]+row_split[2] - 1)
		data['destination_start'].append(row_split[0])
		data['destination_end'].append(row_split[0]+row_split[2] - 1)
		data['range_length'].append(row_split[2])

	return pd.DataFrame(data).sort_values(by = 'source_start')

def find_next(inp_code, df) -> int:

	for row in df.iterrows():

		if inp_code >= row[1]['source_start'] and inp_code <= row[1]['source_end']:
			
			return row[1]['destination_start'] + inp_code - row[1]['source_start']

	return inp_code

def find_next_list(inp_range, df) -> list:

	source_from, source_to = inp_range[0], inp_range[1]

	exit_range = []


	if source_to < min(df['source_start']) or source_from > max(df['source_end']):

		exit_range.append((source_from, source_to))

	if source_from < min(df['source_start']) <= source_to:

		exit_range.append((source_from, min(df['source_start']) - 1))

	if source_to > max(df['source_end']) >= source_from:

		exit_range.append((max(df['source_end']) + 1, source_to))


	for row in df.iterrows():


		r_start, r_end, d_start, d_end = row[1]['source_start'], row[1]['source_end'], row[1]['destination_start'], row[1]['destination_end']

		if source_from <= r_start <= source_to <= r_end:

			exit_range.append((d_start, find_next(source_to, df)))

		elif source_from <= r_start <= r_end <= source_to:

			exit_range.append((d_start, d_end))

		elif r_start <= source_from <= r_end <= source_to:

			exit_range.append((find_next(source_from, df), d_end))

		elif r_start <= source_from <= source_to <= r_end:

			exit_range.append((find_next(source_from, df), find_next(source_to, df)))

	return list(set(exit_range))


def collect_ranges(inp_ranges, df) -> list:

	all_ranges = []

	for inp_range in inp_ranges:

		all_ranges.extend(find_next_list(inp_range,df))

	return list(set(tuple(i) for i in all_ranges))


@timeit
def star_1(file_name) -> int:

	with open(file_name, 'r') as f:

		data = [i.strip() for i in f.read().split('\n\n')]

	seeds = [int(i) for i in data[0].split()[1:]]

	seed_to_soil = create_df(data[1])
	soil_to_fertilizer = create_df(data[2])
	fertilizer_to_water = create_df(data[3])
	water_to_light = create_df(data[4])
	light_to_temperature = create_df(data[5])
	temperature_to_humidity = create_df(data[6])
	humidity_to_location = create_df(data[7])

	location = []

	for seed in seeds:

		soil = find_next(seed, seed_to_soil)
		fertilizer = find_next(soil, soil_to_fertilizer)
		water = find_next(fertilizer, fertilizer_to_water)
		light = find_next(water, water_to_light)
		temperature = find_next(light, light_to_temperature)
		humidity = find_next(temperature, temperature_to_humidity)

		location.append(find_next(humidity, humidity_to_location))

	return min(location)


@timeit
def star_2(file_name) -> int:

	with open(file_name, 'r') as f:

		data = [i.strip() for i in f.read().split('\n\n')]


	seed_to_soil = create_df(data[1])
	soil_to_fertilizer = create_df(data[2])
	fertilizer_to_water = create_df(data[3])
	water_to_light = create_df(data[4])
	light_to_temperature = create_df(data[5])
	temperature_to_humidity = create_df(data[6])
	humidity_to_location = create_df(data[7])

	seed_range = []
	seed = []

	for i, j in enumerate(data[0].split()[1:]):

		if len(seed) == 1:

			seed.append(int(j) + seed[0] - 1)

		else:

			seed.append(int(j))

		if (i+1)%2 == 0:
			seed_range.append(seed)
			seed = []

	soil = collect_ranges(seed_range, seed_to_soil)
	fertilizer = collect_ranges(soil, soil_to_fertilizer)
	water = collect_ranges(fertilizer, fertilizer_to_water)
	light = collect_ranges(water, water_to_light)
	temperature = collect_ranges(light, light_to_temperature)
	humidity = collect_ranges(temperature, temperature_to_humidity)
	location = collect_ranges(humidity, humidity_to_location)

	return min([i[0] for i in location])

if __name__ == '__main__':
	
	print(f"Star 1: {star_1('day_5.txt')}")
	print(f"Star 2: {star_2('day_5.txt')}")