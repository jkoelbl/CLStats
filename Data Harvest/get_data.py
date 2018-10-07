import openpyxl, sys, os
from classes import site_new, site_old, site_sh

OUTPUT = '../../CSVs/output.csv'
DUPES = '../../CSVs/dupes.csv'

def write_to_file(sites):
	[print(str(site),'\n') for site in sites]
	with open(OUTPUT, 'a') as file:
		[file.write(str(site)) for site in sites]

def get_information(path):
	wb = openpyxl.load_workbook(filename=path, read_only=True, data_only=True)
	if not wb['Site Info']['E3'].value:	# is old survey
		print('    { OLD }')
		return site_old(wb)
	if wb[wb.sheetnames[1]]['K47'].value: # is sh/sslc survey
		print('    { SH/SSLC }')
		return site_sh(wb)
	print('    { NEW }')
	return site_new(wb)	# is current survey

def get_all_data():
	# get upper directory
	os.chdir('..')
	ROOT = os.getcwd()+'/'
	os.chdir('Code - Data Harvest')
	
	#clear files
	open(DUPES,'w').close()
	open(OUTPUT, 'w').close()
	
	# get all paths listed as sys arg
	PATHS = [ROOT+arg for arg in sys.argv[1:]]
	sites, items_added = [], {}
	for PATH in PATHS:
		print(PATH)
		for file in os.listdir(PATH):
			# run if data is excel file
			if not os.path.isdir(file) and file.split('.')[-1] == 'xlsx' and file[:2] != '~$':
				print(' ',file)
				site = get_information(path=PATH+'/'+file)
				if site.id not in items_added:
					items_added[site.id] = len(sites)
					sites.append(site)
				else: #if site exists, log and overwrite
					sites[items_added[site.id]] = site
					with open('dupes.csv','a') as dupe:
						dupe.write('\"'+PATH+'\",\"'+file+'\"\n')
	
	# convert to list and sort
	sites.sort(key=lambda x : str(x.id))
	
	# write to output.csv
	write_to_file(sites)

get_all_data()