from .auxillary_functions import *

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

def get_total_site_access(sites):
	access = {type:[0 for _ in range(7)] for type in access_types}
	for site in sites:
		access_type = get_site_access(site)
		access[access_type][site.site_size] += 1
	access = {access_types_extended[i]:access[access_types[i]] for i in range(len(access_types))}
	return access
