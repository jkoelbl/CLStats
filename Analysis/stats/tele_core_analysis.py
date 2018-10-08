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
