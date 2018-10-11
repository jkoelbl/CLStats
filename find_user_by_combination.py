from Analysis.formatting import load_data
from Analysis.stats.auxillary_functions import *

ROOT = 'C:\\Users\\acesp\\Desktop\\Site Survey Responses\\CSVs/'
PATH = ROOT+'Site Summary 100418 v4.csv'

def get_agents(site):
	a1,a2,c1,c2 = 0,0,0,0
	comp = ('basic','advanced')
	for program in site.programs:
		if program.telephony_users.platform == 'avaya':
			a1+=program.telephony_users.total
		elif program.telephony_users.platform == 'cisco':
			c1+=program.telephony_users.total
		if program.cc_complexity.complexity in comp:
			if program.contact_center.platform == 'avaya':
				a2+=program.contact_center.total
			elif program.contact_center.platform == 'cisco':
				c2+=program.contact_center.total
	return a1,a2,c1,c2

def refine_sites():
	sites = load_data(PATH)
	map = {}
	for site in sites:
		key = site.avaya_type
		combo = determine_platform_combination(site)
		ua = get_agents(site)
		if key not in map:
			map[key] = {}
		if combo not in map[key]:
			map[key][combo] = [0,0,0,0]
		map[key][combo] = [map[key][combo][i]+ua[i] for i in range(4)]
	return map

def print_mix():
	map = refine_sites()
	maps = [{} for _ in range(6)]
	for k,v in map.items():
		index = 0
		if k in ('remote moreton','remote winters','moreton core','winters core'):
			index = 3
		for c,data in v.items():
			if c in ('A','A+Acc','Acc'):
				maps[0+index][c] = data
			elif c in ('C','C+Ccc','Ccc'):
				maps[1+index][c] = data
			else:
				maps[2+index][c] = data
	types = ('cores+avaya','cores+cisco','cores+other','noncores+avaya','noncores+cisco','noncores+other')
	for i in range(len(maps)):
		print(types[i])
		[print('\t\''+k+'\'\t'+str(v)) for k,v in maps[i].items()]

print_mix()
