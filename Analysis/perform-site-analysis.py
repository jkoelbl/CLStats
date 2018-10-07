"""
	-add update data
	-number of sites used (eventually)
	-add survivablitity in data (not sure)
	-add 2 columns: "is survivable (y,n)" and "survivable type"
"""

from save import *
from statistics import *
from formatting_v2 import load_data, make_classes

INFILE = '../../CSVs/Site Summary 100418 v4-pivot.csv'
OUTFILE = '../../CSVs/results.csv'

# load data and convert to classes
sites = load_data(INFILE)


# perform analyses
region_sizes, site_sizes, program_sizes, platform_sizes, cc_platform_sizes = get_site_size_analysis(sites)
bis_users, cc_users, cs, omt, role_total, avg_workers_at_avaya = get_user_analysis(sites)
site_complexities = get_complexity_analysis(sites)
business_functions, bis_func_counts = get_business_function_analysis(sites)
events = get_event_analysis(sites)
site_access = get_site_access_analysis(sites)
num_owned = get_owned_status_analysis(sites)
bis_cc_type, bis_cc_type_connectivity = get_bis_cc_analysis(sites)
cc_types_extended, agency_per_type = get_lead_agency_analysis(sites)
tele_core = get_tele_core_analysis(sites)

# save result as comma-separated list
output = init_outfile()
output += add_new_data('Number of Sites,'+encode_list(site_sizes), newline=False)
output += add_new_data(encode_maplist_w_sum(region_sizes), title='Number of Sites per Region')
output += add_new_data(encode_maplist_w_sum(program_sizes), title='Number of Sites with a Given Number of Programs')
output += add_new_data(encode_maplist_w_sum(platform_sizes), title='Number of Sites with a Given Business Telephony Platform')
output += add_new_data(encode_maplist_w_sum(cc_platform_sizes), title='Number of Sites with a Given Contact Center Platform')

output += add_new_data(encode_maplist_w_sum(bis_users), title='Number of Business Telephony Users per Site Size')
output += add_new_data(encode_maplist_w_sum(cc_users), title='Number of Contact Center Users per Site Size')
output += add_new_data(encode_maplist(cs, False), title='Average Number of Contractors/Staff at a Given Site')
output += add_new_data(encode_maplist(omt, False), title='Average Number of Onsite Workers/Mobile Workers/Telecommuters at a Given Site')

output += add_new_data(encode_maplist_w_sum(site_complexities), title='Contact Center Complexities')
output += add_new_data(encode_multilist(bis_func_counts), title='Number of Sites with Given Number of Business Functions')
for k in business_functions.keys():
	output += add_new_data(encode_maplist(business_functions[k]), title='Business functions - '+k+' Responses')

output += add_new_data(encode_maplist_w_sum(events), title='Number of Sites with Given Site Event Contingency')
output += add_new_data(encode_maplist_w_sum(site_access), title='Site Access')
output += add_new_data(encode_maplist_w_sum(num_owned), title='Number of Sites Owned/Leased by Site Size')

output += add_new_data(encode_maplist_w_sum(bis_cc_type), title='Number of Sites with Given Business and Contact Center Platforms')
for k,v in bis_cc_type_connectivity.items():
	output += add_new_data(encode_maplist_w_sum(v), title='Number of Sites with Given Connectivity: Business and Contact Center Platforms - ' + str(k))

output += add_new_data(encode_maplist_w_sum(role_total), title='Total Number of Workers per Role')
header = ','+','.join(cc_types_extended)+',total\n'
output += add_new_data(header+encode_maplist_w_sum(agency_per_type), title='Number of Sites with a Given Lead Agency by Business/Contact Center Platform')

output += add_new_data(encode_maplist_w_sum(tele_core), title='Avaya by Telephony Core')
output += add_new_data(encode_maplist(avg_workers_at_avaya, False), title='Average Number of Workers at Sites with Avaya Business and Avaya Contact Center Only')

# print output and save it in OUTFILE
print(output)
with open(OUTFILE, 'w') as file:
	file.truncate(0)
	file.write(output)
