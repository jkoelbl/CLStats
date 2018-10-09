import csv,os
from formatting import load_data

past_dir = os.getcwd()
os.chdir('../../CSVs/')
ROOT = os.getcwd()+'/'
os.chdir(past_dir)

base_files = ('Moreton-A','Moreton-A+Acc','Winters-A','Winters-A+Acc','Moreton-100+','Winters-100+')
PATHS = [ROOT+'Tele Core Sites/'+file+'.csv' for file in base_files]
SITES = ROOT+'Site Summary 100418 v4.csv'
GATEWAYS = ROOT+'Site Status 100518 v1.csv'

def init_files():
	for path in PATHS:
		open(path,'w').close()
	files = [open(path, 'a') for path in PATHS]
	for file in files:
		file.write('\"Site ID\",\"Total business Users\",\"Total CC Agents\",G430,G450,G650,G700')
	return files
	
	
def get_gateways(path):
	with open(path, newline='') as file:
		reader = csv.reader(file, delimiter=',', quotechar='\"')
		return {row[0]:row[19:23] for row in reader}

def get_total_users_agents(site):
	users, agents = 0,0
	for program in site.programs:
		users += program.telephony_users.total
		agents += program.contact_center.total
	return users, agents
	
def get_combo(site):
	comb = ('basic','advanced')
	temp_b, temp_cc = {}, {}
	for program in site.programs:
		temp_b[program.telephony_users.platform] = None
		if program.cc_complexity.complexity in comb and program.contact_center.total:
			temp_cc[program.contact_center.platform] = None
	if 'avaya' in temp_b and 'cisco' not in temp_b:
		if 'avaya' in temp_cc and 'cisco' not in temp_cc:
			return 'A+Acc'
		return 'A'
	return ''

def get_tele_core(site):
	if site.avaya_type in ('remote winters', 'winters core'):
		return 'winters'
	if site.avaya_type in ('remove moreton', 'moreton core'):
		return 'moreton'
	return ''

def get_base_critera(site):
	index = 0
	combo = get_combo(site)
	if site.avaya_type in ('moreton core','remote moreton'):
		index = 0
	elif site.avaya_type in ('winters core','remote winters'):
		index = 2
	else:	return ''
	
	if combo == 'A':
		return index
	elif combo == 'A+Acc':
		return index+1
	return ''

def add_to_file(site, gateways, files):
	criteria = get_base_critera(site)
	core = get_tele_core(site)
	users, agents = get_total_users_agents(site)
	gtw = ['','','','']
	
	if criteria=='':	return
	if criteria in (0,2):	agents = 0
	if str(int(site.id)) in gateways:	gtw = gateways[str(int(site.id))]
	else:	print('issue:', str(site.id), 'not in gateways list')
	
	group = [int(site.id), users, agents] + gtw
	output = ','.join([str(g) for g in group])
	files[criteria].write('\n'+output)
	
	if site.site_size > 3:
		if core == 'moreton':
			files[4].write('\n'+output)
		elif core == 'winters':
			files[5].write('\n'+output)
	
if __name__ == '__main__':
	files = init_files()
	sites = load_data(SITES)
	gateways = get_gateways(GATEWAYS)
	for site in sites:	add_to_file(site, gateways, files)
	for file in files:	file.close()
	print('done')
