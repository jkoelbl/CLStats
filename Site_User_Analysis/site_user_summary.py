import csv,os
from .formatting import load_data

ROOT = 'C:\\Users\\acesp\\Desktop\\Site Survey Responses\\CSVs/'
base_files = ('Moreton (Avaya - 1-100)','Moreton (Avaya - 101+)','Winters (Avaya - 1-100)','Winters (Avaya - 101+)')
PATHS = [ROOT+'Tele Core Sites/'+file+'.csv' for file in base_files]
SITES = ROOT+'Site Summary 100418 v4.csv'
GATEWAYS = ROOT+'Site Status 100518 v1.csv'
tSize = ('XXS','XS','S','M','L','XL','XXL')

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
		return {row[0]:row[19:23] for row in reader}

def get_total_users_agents(site):
	users, agents = 0,0
	comp = ('basic','advanced')
	for program in site.programs:
		if program.telephony_users.platform == 'avaya':
			users += program.telephony_users.total
		if program.cc_complexity.complexity in comp and program.contact_center.platform == 'avaya':
			agents += program.contact_center.total
	return users, agents
	
def get_combo(site):
	comp = ('basic','advanced')
	temp_b, temp_cc = {}, {}
	for program in site.programs:
		temp_b[program.telephony_users.platform] = None
		if program.cc_complexity.complexity in comp and program.contact_center.total:
			temp_cc[program.contact_center.platform] = None
	if 'avaya' in temp_b and 'cisco' not in temp_b:
		if 'avaya' in temp_cc and 'cisco' not in temp_cc:
			return 'A+Acc'
		return 'A'
	if 'avaya' in temp_cc and 'cisco' not in temp_cc:
		return 'Acc'
	return ''

def get_base_critera(site):
	moreton = ('moreton core','remote moreton')
	winters = ('winters core','remote winters')
	index = 0
	if get_combo(site) not in ('A','A+Acc','Acc'):	return ''
	if site.avaya_type in moreton:	index = 0
	elif site.avaya_type in winters:	index = 1
	else:	return ''
	
	if site.site_size<4:	return index*2
	else:	return index*2+1

def add_to_file(site, gateways, files):
	criteria = get_base_critera(site)
	combo = get_combo(site)
	users, agents = get_total_users_agents(site)
	tshirt = tSize[site.site_size]
	gtw = ['','','','']
	
	if criteria=='':	return
	if combo == 'A':	agents = ''
	elif combo == 'Acc':	users = ''
	if str(site.id) in gateways:	gtw = gateways[str(site.id)]
	else:	print('issue:', str(site.id), 'not in gateways list')
	
	group = [site.id, '\"'+site.addr+'\"', tshirt, users, agents] + gtw + [site.total]
	output = ','.join([str(g) for g in group])
	files[criteria].write('\n'+output)

def user_summary():
	files = init_files()
	sites = load_data(SITES)
	gateways = get_gateways(GATEWAYS)
	for site in sites:	add_to_file(site, gateways, files)
	for file in files:	file.close()
	print('done')

if __name__ == '__main__':
	user_summary()