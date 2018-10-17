from Common.auxillary_functions import *

cc_types = ('C', 'C+Ccc', 'C+Acc', 'C+C/Acc', \
			'A', 'A+Ccc', 'A+Acc', 'A+C/Acc', \
			'C/A', 'C/A+Ccc', 'C/A+Acc', 'C/A+C/Acc', \
			'Ccc', 'Acc', 'C/Acc', '')
cc_types_extended = ('Cisco Business Only', \
			'Cisco Business and Cisco Contact Center Only', \
			'Cisco Business and Avaya Contact Center Only', \
			'Cisco Business and Cisco and Avaya Contact Center Only', \
			'Avaya Business Only', \
			'Avaya Business and Cisco Contact Center Only', \
			'Avaya Business and Avaya Contact Center Only', \
			'Avaya Business and Cisco and Avaya Contact Center Only', \
			'Cisco and Avaya Business Only', \
			'Cisco and Avaya Business and Cisco Contact Center Only', \
			'Cisco and Avaya Business and Avaya Contact Center Only', \
			'Cisco and Avaya Business with Cisco and Avaya Contact Center Only', \
			'Cisco Contact Center Only', \
			'Avaya Contact Center Only', \
			'Cisco and Avaya Contact Center Only', \
			'None')

def get_num_owned(sites):
	types = ('owned', 'leased', 'none')
	num_owned = {type:[0 for _ in range(7)] for type in types}
	for site in sites:
		status = site.is_leased
		if not status:	status = 'none'
		num_owned[status][site.site_size] += 1
	types_extended = ('Owned', 'Leased', 'None')
	num_owned = {types_extended[i]:num_owned[types[i]] for i in range(len(types))}
	return num_owned

def get_agency_per_type(sites):
	temp, apt = {}, {}
	
	# get lead agency, contact center pairs and load into double map
	for site in sites:
		site_type = determine_platform_combination(site)
		if site.lead_agency not in temp:
			temp[site.lead_agency] = {}
			apt[site.lead_agency] = [0 for _ in cc_types]
		if site_type not in temp[site.lead_agency]:
			temp[site.lead_agency][site_type] = 0
		temp[site.lead_agency][site_type] += 1
	
	# load values into maplist
	for agency in apt.keys():
		for i in range(len(cc_types)):
			if cc_types[i] in temp[agency]:
				apt[agency][i] = temp[agency][cc_types[i]]
	apt = {k.upper():v for k,v in apt.items()}
	
	# convert incorrect capitalizations
	temp, temp2 = ('MULTIPLE', ''), ('Multiple', 'None')
	for i in range(len(temp)):	
		if temp[i] in apt:
			apt[temp2[i]] = apt[temp[i]]
			del apt[temp[i]]
	return apt

def get_poe(sites):
	types = ('Yes','Some','No','')
	poe_cap = {type:[0 for _ in range(7)] for type in types}
	for site in sites:
		poe_cap[site.poe_capable][site.site_size] += 1
	return poe_cap
