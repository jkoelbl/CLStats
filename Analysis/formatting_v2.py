import os,csv
from .classes_v2 import site

# check if two rows are duplicates
def is_dupe(ref, row):
	for i in range(len(ref)):
		if row[i] != ref[i]:
			return False
	return True

# check if a row is empty
def is_empty(row):
	for i in range(len(row)):
		if row[i]:
			return False
	return True

# open csv and read raw data
def get_raw_data(path):
	with open(path, newline='') as file:
		reader = csv.reader(file, delimiter=',', quotechar='\"')
		list = [[item.strip() for item in row] for row in reader if not is_empty(row)]
		return list[:]	#[2:]

# convert numbers to ints
def convert_nums(list_csv):
	for row in list_csv:
		for i in range(len(row)):
			try:	row[i] = int(row[i])
			except ValueError:	row[i] = row[i].lower()
	return list_csv

# remove empty entries
def remove_empties(list_csv):
	for i in range(len(list_csv)-1, -1, -1):
		is_none = True
		for item in list_csv[i][7:]:
			is_none = not item or item == '0'
			if item:	break
		if is_none:	del list_csv[i]
	return list_csv

# fill missing string data with related data
def fill_missing_site_data(list_csv):
	site = list_csv[0][:7]
	for row in list_csv:
		if is_empty(row[:7]):
			for i in range(len(site)):
				row[i] = site[i]
		else:
			site = row[:7]
	return list_csv

# fill missing business function responses with 'No'
def fill_missing_bis_func(list_csv):
	for row in list_csv:
		for i in range(10,21):
			if not row[i]: row[i] = 'no'
	return list_csv

# fill missing numerical data with 0's
def fill_missing_num_data(list_csv):
	for row in list_csv:
		for i in range(23,29):
			if not row[i]:	row[i] = 0
			if not row[i+7]:	row[i+7] = 0	#+9
	return list_csv

# modify duplicates for uniqueness
def adjust_for_dupes(list_csv):
	site = list_csv[0][:7]
	for row in list_csv:
		if not is_dupe(row[:7], site):
			if row[0] == site[0]:
				row[0] = row[0]+.1
			else:
				for i in range(len(site)):
					site[i] = row[i]
	return list_csv

# repairs platforms with valid names
def fix_platforms(list_csv):
	cisco = ['cisco', 'cicso', 'hsc', 'hcs']
	for row in list_csv:
		if row[22].lower() in cisco:	row[22] = 'cisco'
		if row[29].lower() in cisco:	row[29] = 'cisco'	#31
	return list_csv

# loads the data into a formatted 2d-list
def load_data(path):
	list_csv = get_raw_data(path)
	list_csv = remove_empties(list_csv)
	list_csv = fill_missing_site_data(list_csv)
	list_csv = fill_missing_bis_func(list_csv)
	list_csv = fix_platforms(list_csv)
	list_csv = fill_missing_num_data(list_csv)
	list_csv = convert_nums(list_csv)
	list_csv = adjust_for_dupes(list_csv)
	return make_classes(list_csv[1:])

# converts data list into site objects
def make_classes(list_csv):
	sites = [site(list_csv[0])]
	for row in list_csv:
		if sites[-1].id != row[0]:
			sites.append(site(row))
		sites[-1].new_program(row)
	return sites
