from Common.auxillary_functions import *

platform_types = ('cisco', 'avaya', 'both', 'none')
platform_types_extended = ('Cisco', 'Avaya', 'Both', 'None')

def get_regional_site_sizes(sites):
	types = [i for i in range(12)] + ['sh','sslc','']
	region_sizes = {type:[0 for _ in range(7)] for type in types}
	for site in sites:
		region_sizes[site.region][site.site_size] += 1
	return region_sizes

def get_site_sizes(region_sizes):
	size_totals = [0 for _ in range(7)]
	for k in region_sizes.values():
		for i in range(len(k)):
			size_totals[i] += k[i]
	return size_totals

def get_program_site_sizes(sites):
	types = [i for i in range(11)] + ['>10']
	program_sizes = {type:[0 for _ in range(7)] for type in types}
	for site in sites:
		num_programs = '>10' if len(site.programs) > 10 else len(site.programs)
		program_sizes[num_programs][site.site_size] += 1
	return program_sizes

def get_platform_sizes(sites, get_platform):
	platform_sizes = {platform:[0 for _ in range(7)] for platform in platform_types}
	for site in sites:
		platform = get_platform(site)
		platform_sizes[platform][site.site_size] += 1
	platform_sizes = {platform_types_extended[i]:platform_sizes[platform_types[i]] for i in range(len(platform_types))}
	return platform_sizes
