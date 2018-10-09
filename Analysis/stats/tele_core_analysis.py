from .auxillary_functions import *

avaya_types = ('winters core','moreton core','remote winters','remote moreton','self','')
avaya_types_extended = ('Winters CORE','Moreton CORE','Remote Winters','Remote Moreton','Self','None')

def get_tele_core_data(sites):
	data = {type:[0 for _ in range(7)] for type in avaya_types}
	for site in sites:
		data[site.avaya_type][site.site_size] += 1
	data = {avaya_types_extended[i]:data[avaya_types[i]] for i in range(len(avaya_types))}
	return data

def get_bis_tele_core_data(sites):
	data = {type:[0 for _ in range(7)] for type in avaya_types}
	for site in sites:
		platform = determine_platform_combination(site)
		if platform == 'A':
			data[site.avaya_type][site.site_size] += 1
	data = {avaya_types_extended[i]:data[avaya_types[i]] for i in range(len(avaya_types))}
	return data
	
def get_cc_tele_core_data(sites):
	data = {type:[0 for _ in range(7)] for type in avaya_types}
	for site in sites:
		platform = get_cc_platform(site)
		if platform == 'avaya':
			data[site.avaya_type][site.site_size] += 1
	data = {avaya_types_extended[i]:data[avaya_types[i]] for i in range(len(avaya_types))}
	return data

def get_tele_core(site):
	if site.avaya_type in ('moreton core','remote moreton'):
		return 'moreton'
	if site.avaya_type in ('winters core','remote winters'):
		return 'winters'
	return ''


def format_avg_tele_core_users(data):
	for i in range(len(tele_types)):
		data[tele_types_extended[i]] = data[tele_types[i]]
		del data[tele_types[i]]
		for j in range(len(comb)):
			data[tele_types_extended[i]][comb_extended[j]] = data[tele_types_extended[i]][comb[j]]
			del data[tele_types_extended[i]][comb[j]]
			for k in range(len(user_types)):
				data[tele_types_extended[i]][comb_extended[j]][user_types_extended[k]] = data[tele_types_extended[i]][comb_extended[j]][user_types[k]]
				del data[tele_types_extended[i]][comb_extended[j]][user_types[k]]
	return data

def get_tele_core_users(sites):
	tele_types = ('moreton', 'winters')
	comb = ('A','A+Acc')
	user_types = ('bis users','cc agents')
	data = {type:{combo:{user:[0 for _ in range(7)] for user in user_types} data for combo in comb} for type in tele_types}
	total_sites = {type:{combo:[0 for _ in range(7)] for combo in comb} for type in tele_types}
	
	for site in sites:
		tele_core = get_tele_core(site)
		combo = determine_platform_combination(site)
		users, agents = get_users_agents(sites)
		if combo in comb and tele_core in tele_types:
			data[tele_core][combo]['bis users'] += users
			data[tele_core][combo]['cc agents'] += agents
			data[tele_core][combo] += 1
	
	for type in tele_types:
		for combo in comb:
			total = total_sites[type][combo] if total_sites[type][combo] else 1
			data[type][combo]['bis users'] /= total
			data[type][combo]['cc agents'] /= total

	return format_avg_tele_core_users(data)