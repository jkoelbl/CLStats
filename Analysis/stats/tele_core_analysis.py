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

def get_avg_tele_core_users(data, total_sites):
	tele_types = ('moreton', 'winters')
	comb = ('A','A+Acc')
	for combo in comb:
		for type in tele_types:
			for size in range(7):
				total = total_sites[combo][type][size] if total_sites[combo][type][size] else 1
				data[combo][type]['bis users'][size] = round(data[combo][type]['bis users'][size]/total, 1)
				data[combo][type]['cc agents'][size] = round(data[combo][type]['cc agents'][size]/total, 1)
	return data

def format_avg_tele_core_users(data):
	tele_types = ('moreton', 'winters')
	tele_types_extended = ('Moreton Sites', 'Winters Sites')
	comb = ('A','A+Acc')
	comb_extended = ('Avaya Business Only', 'Avaya Business with Avaya Contact Center Only')
	user_types = ('bis users','cc agents')
	user_types_extended = ('Business Telephony Users', 'Contact Center Agents')
	for i in range(len(comb)):
		data[comb_extended[i]] = data[comb[i]]
		del data[comb[i]]
		for j in range(len(tele_types)):
			data[comb_extended[i]][tele_types_extended[j]] = data[comb_extended[i]][tele_types[j]]
			del data[comb_extended[i]][tele_types[j]]
			for k in range(len(user_types)):
				data[comb_extended[i]][tele_types_extended[j]][user_types_extended[k]] = data[comb_extended[i]][tele_types_extended[j]][user_types[k]]
				del data[comb_extended[i]][tele_types_extended[j]][user_types[k]]
	return data

def get_tele_core_users(sites):
	tele_types = ('moreton', 'winters')
	comb = ('A','A+Acc')
	user_types = ('bis users','cc agents')
	data = {combo:{type:{user:[0 for _ in range(7)] for user in user_types} for type in tele_types} for combo in comb}
	total_sites = {combo:{type:[0 for _ in range(7)] for type in tele_types} for combo in comb}
	
	for site in sites:
		tele_core = get_tele_core(site)
		combo = determine_platform_combination(site)
		users, agents = get_users_agents(site)
		if combo == 'A':	agents = 0
		if combo in comb and tele_core in tele_types:
			data[combo][tele_core]['bis users'][site.site_size] += users
			data[combo][tele_core]['cc agents'][site.site_size] += agents
			total_sites[combo][tele_core][site.site_size] += 1
	
	data = get_avg_tele_core_users(data, total_sites)
	return format_avg_tele_core_users(data)