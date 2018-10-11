import csv,os
from Common.formatting import *
from Common.auxillary_functions import *

ROOT = 'C:\\Users\\acesp\\Desktop\\Site Survey Responses\\CSVs/'
base_files = ('Moreton (Avaya - 1-100)','Moreton (Avaya - 101+)','Winters (Avaya - 1-100)','Winters (Avaya - 101+)','Moreton (Mix - 1-100)','Moreton (Mix - 101+)','Winters (Mix - 1-100)','Winters (Mix - 101+)','Self','Other','Avaya - No Core')
PATHS = [ROOT+'Tele Core Sites/'+file+'.csv' for file in base_files]
SITES = ROOT+'Site Summary 100418 v4.csv'
GATEWAYS = ROOT+'Site Status 100518 v1.csv'
tSize = ('XXS','XS','S','M','L','XL','XXL')
moreton = ('moreton core','remote moreton','moreton')
winters = ('winters core','remote winters','winters')
ADD_CISCO_NUMBERS = [0,0,0,0,1,1,1,1,1,1,0]
cisco = ('C','Ccc','C+Ccc')
avaya = ('A','Acc','A+Acc')

def init_files(paths, add_cisco):
	for path in paths:
		open(path,'w').close()
	files = [open(path, 'a') for path in PATHS]
	for i in range(len(files)):
		if add_cisco[i]:
			files[i].write('\"Site ID\",\"Address\",\"t-Shirt\",\"Total Avaya Business Users\",\"Total Avaya CC Agents\",\"Total Cisco Business Users\",\"Total Cisco Business Agents\",G430,G450,G650,G700,Total Users')
		else:
			files[i].write('\"Site ID\",\"Address\",\"t-Shirt\",\"Total Avaya Business Users\",\"Total Avaya CC Agents\",G430,G450,G650,G700,Total Users')
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

def get_base_critera(site, combo):
	index = 0
	if combo in cisco or combo == '':	return ''
	
	if site.avaya_type in moreton:
		if combo in avaya:	index = 0
		else:	index = 2
	elif site.avaya_type in winters:
		if combo in avaya:	index = 1
		else:	index = 3
	elif site.avaya_type == 'self':
		return 8
	else:
		if combo in avaya:	return 10
		else:	return 9
	
	if site.site_size<4:	return index*2
	else:	return index*2+1

def refine_ua(ua, combo):
	return [x if x else '' for x in ua]

def add_to_file(site, gateways, files):
	combo = determine_platform_combination(site)
	criteria = get_base_critera(site, combo)
	ua = get_total_users_agents(site)
	tshirt = tSize[site.site_size]
	gtw = ['','','','']
	group = [site.id, '\"'+site.addr+'\"', tshirt]
	
	if criteria=='':	return
	if str(site.id) in gateways:
		gtw = gateways[str(site.id)]
	else:
		print('issue:', str(site.id), 'not in gateways list')
	
	if criteria in (0,1,2,3,10):
		group += refine_ua(ua[:2], combo)
		group += gtw
		group += [sum(ua[:2])]
	else:
		group += refine_ua(ua, combo)
		group += gtw
		group += [sum(ua)]
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
