import csv,os
from Common.formatting import *
from Common.auxillary_functions import *

ROOT = 'C:\\Users\\acesp\\Desktop\\Site Survey Responses\\CSVs/'
base_files = ('Moreton (Avaya - 1-100)','Moreton (Avaya - 101+)','Winters (Avaya - 1-100)','Winters (Avaya - 101+)')
PATHS = [ROOT+'Tele Core Sites/'+file+'.csv' for file in base_files]
SITES = ROOT+'Site Summary 100418 v4.csv'
GATEWAYS = ROOT+'Site Status 100518 v1.csv'
tSize = ('XXS','XS','S','M','L','XL','XXL')
moreton = ('moreton core','remote moreton','moreton')
winters = ('winters core','remote winters','winters')

def init_files():
	for path in PATHS:
		open(path,'w').close()
	files = [open(path, 'a') for path in PATHS]
	for file in files:
		file.write('\"Site ID\",\"Address\",\"t-Shirt\",\"Total business Users\",\"Total CC Agents\",G430,G450,G650,G700,Total Users')
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
				agents += program.contact_center.total
			elif program.contact_center.platform == 'cisco':
				agents += program.contact_center.total
	return ua

def get_base_critera(site, combo):
	index = 0
	if combo not in ('A','A+Acc','Acc'):	return ''
	if site.avaya_type in moreton:	index = 0
	elif site.avaya_type in winters:	index = 1
	else:	return ''
	
	if site.site_size<4:	return index*2
	else:	return index*2+1

def add_to_file(site, gateways, files):
	combo = determine_platform_combination(site)
	criteria = get_base_critera(site, combo)
	users, agents = get_total_users_agents(site)
	tshirt = tSize[site.site_size]
	group = [site.id, '\"'+site.addr+'\"', tshirt]
	gtw = ['','','','']
	
	if criteria=='':	return
	if combo == 'A':	agents = ''
	elif combo == 'Acc':	users = ''
	if str(site.id) in gateways:	gtw = gateways[str(site.id)]
	else:	print('issue:', str(site.id), 'not in gateways list')
	
	group += ua[:2] + gtw + [site.total]
	output = ','.join([str(g) for g in group])
	files[criteria].write('\n'+output)

def user_summary():
	files = init_files()
	sites = load_data(SITES)
	sites = make_classes(sites)
	gateways = get_gateways(GATEWAYS)
	for site in sites:	add_to_file(site, gateways, files)
	for file in files:	file.close()
	print('done')

if __name__ == '__main__':
	user_summary()
