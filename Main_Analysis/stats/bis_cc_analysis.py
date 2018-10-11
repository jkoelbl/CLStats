from Common.auxillary_functions import *

access_types = ('ethernet', \
				'isdn pri', \
				'gigabit ethernet', \
				't1', \
				'ds3', \
				'oc3', \
				'fast ethernet', \
				'cable', \
				'multiple', \
				'none')
access_types_extended = ('Ethernet', \
					'ISDN/PRI', \
					'Gigabit Ethernet', \
					'T1', \
					'DS3', \
					'OC3', \
					'Fast Ethernet', \
					'Cable', \
					'Multiple', \
					'None')
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


def get_bis_cc_type(sites):
	bcct = {type:[0 for _ in range(7)] for type in cc_types}
	for site in sites:
		index = determine_platform_combination(site)
		bcct[index][site.site_size] += 1
	bcct = {cc_types_extended[i]:bcct[cc_types[i]] for i in range(len(cc_types_extended))}
	return bcct

def get_connectivity_type_given_bis_cc_type(sites):
	bcct_connect = {type:{at:[0 for _ in range(7)] for at in access_types} for type in cc_types}
	for site in sites:
		reporting = get_site_access(site)
		bcc_type = determine_platform_combination(site)
		bcct_connect[bcc_type][reporting][site.site_size] += 1
	
	bcct_connect = {cc_types_extended[i]:bcct_connect[cc_types[i]] for i in range(len(cc_types))}
	for k in bcct_connect.keys():
		bcct_connect[k] = {access_types_extended[i]:bcct_connect[k][access_types[i]] for i in range(len(access_types))}
	return bcct_connect
