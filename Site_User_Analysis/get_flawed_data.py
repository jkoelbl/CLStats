import csv,os
from Common.auxillary_functions import *
from Common.formatting import *
from Site_User_Analysis import *

ROOT = 'C:\\Users\\acesp\\Desktop\\Site Survey Responses\\CSVs/'
base_files = ('Unlisted Core (Avaya - 1-100)', 'Unlisted Core (Avaya - 101+)', 'Unlisted Core (Mix - 1-100)', 'Unlisted Core (Mix - 101+)', 'Moreton (Mix - 1-100)', 'Moreton (Mix - 101+)', 'Winters (Mix - 1-100)', 'Winters (Mix - 101+)')
PATHS = [ROOT+'Tele Core Sites/'+file+'.csv' for file in base_files]
SITES = ROOT+'Site Summary 100418 v4.csv'
GATEWAYS = ROOT+'Site Status 100518 v1.csv'

tSize = ('XXS','XS','S','M','L','XL','XXL')
avaya = ('A','Acc','A+Acc')
cisco = ('C','Ccc','C+Ccc')
ADD_CISCO_NUMBERS = (False, False, True, True, True, True, True, True)
core_types = ('moreton core','remote moreton','winters core','remote winters')
moreton = ('moreton core','remote moreton')
winters = ('winters core','remote winters')

def init_files(paths, add_cisco):
	for path in paths:
		open(path,'w').close()
	files = [open(path, 'a') for path in PATHS]
	for i in range(len(files)):
		if add_cisco[i]:
			files[i].write('\"Site ID\",\"Address\",\"t-Shirt\",\"Total Avaya Cusiness Users\",\"Total Avaya CC Agents\",\"Total Cisco Business Users\",\"Total Cisco CC Users\",G430,G450,G650,G700,Total Users')
		else:
			files[i].write('\"Site ID\",\"Address\",\"t-Shirt\",\"Total Avaya Cusiness Users\",\"Total Avaya CC Agents\",G430,G450,G650,G700,Total Users')
	return files
	
def get_gateways(path):
	with open(path, newline='') as file:
		reader = csv.reader(file, delimiter=',', quotechar='\"')
		return {str(row[0]):row[19:23] for row in reader}

def get_total_users_agents(site):
	ua = [0,0,0,0]
	comp = ('basic','advanced')
	for program in site.programs:
		if program.telephony_users.platform == 'avaya':
			ua[0] += program.telephony_users.total
		elif program.telephony_users.platform == 'cisco':
			ua[2] += program.telephony_users.total
		if program.cc_complexity.complexity in comp:
			if program.contact_center.platform == 'avaya':
				ua[1] += program.contact_center.total
			elif program.contact_center.platform == 'cisco':
				ua[3] += program.contact_center.total
	return ua

def get_base_critera(site):
	index = 0
	combo = determine_platform_combination(site)
	if combo in cisco or combo == '':	return ''
	if site.avaya_type not in core_types:
		if combo in avaya:	index = 0
		else:	index = 1
	elif combo not in avaya:
		if site.avaya_type in moreton:	index = 2
		elif site.avaya_type in winters:	index = 3
	else:	return ''
	
	if site.site_size<4:	return index*2
	else:	return index*2+1

def clean_ua(ua, combo):
	if combo == 'A':
		return [ua[0], '', '', '']
	if combo == 'C/A':
		return [ua[0], ua[1], '', '']
	if combo == 'C/A+Acc':
		return [ua[0], ua[1], ua[2], '']
	if combo == 'C+Acc':
		return ['', ua[1], ua[2], '']
	if combo == 'C+C/Acc':
		return ['', ua[1], ua[2], ua[3]]
	if combo == 'Acc':
		return ['', '', ua[2], '']
	if combo == 'C/Acc':
		return ['', '', ua[2], ua[3]]
	return ua

def add_to_file(site, gateways, files):
	criteria = get_base_critera(site)
	combo = determine_platform_combination(site)
	ua = get_total_users_agents(site)
	tshirt = tSize[site.site_size]
	gtw = ['','','','']
	group = [site.id, '\"'+site.addr+'\"', tshirt]
	
	if criteria=='':	return
	ua = clean_ua(ua, combo)
	if str(site.id) in gateways:	gtw = gateways[str(site.id)]
	else:	print('issue:', str(site.id), 'not in gateways list')
	
	if criteria in (0,1):
		group += ua[:2] + gtw + [site.total]
	else:
		group += ua + gtw + [site.total]
	output = ','.join([str(g) for g in group])
	files[criteria].write('\n'+output)

def user_summary():
	files = init_files(PATHS, ADD_CISCO_NUMBERS)
	sites = load_data(SITES)
	sites = make_classes(sites)
	gateways = get_gateways(GATEWAYS)
	for site in sites:	add_to_file(site, gateways, files)
	for file in files:	file.close()
	print('done')

if __name__ == '__main__':
	user_summary()