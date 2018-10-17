from .stats import *

def get_site_size_analysis(regions):
	region_sizes = get_regional_site_sizes(regions)
	site_sizes = get_site_sizes(region_sizes)
	program_sizes = get_program_site_sizes(regions)
	platform_sizes = get_platform_sizes(regions, get_bis_platform)
	cc_platform_sizes = get_platform_sizes(regions, get_cc_platform)
	return region_sizes, site_sizes, program_sizes, platform_sizes, cc_platform_sizes

def get_user_analysis(regions):
	bis_users = get_platform_users(regions, get_program_bis_platform_total)
	cc_users = get_platform_users(regions, get_program_cc_platform_total)
	
	site_sizes = get_site_sizes(get_regional_site_sizes(regions))
	total_users = get_total_users(regions)
	total_user_types = get_total_user_types(total_users)
	cs = avg_contractors_staff(total_users, site_sizes)
	omt = avg_user_types(total_users, site_sizes)
	
	types = ('A', 'A+Acc', 'C', 'C+Ccc')
	types_extended = ('Avaya Business Only', 'Avaya Business with Avaya Contact Center Only', 'Cisco Business Only', 'Cisco Business with Cisco Contact Center Only')
	avg_workers_with_setup = {types_extended[i]:get_avg_users_with_platform_combo(regions, types[i]) for i in range(len(types))}
	return bis_users, cc_users, cs, omt, total_user_types, avg_workers_with_setup
	
def get_complexity_analysis(regions):
	return get_site_complexities(regions)
	
def get_business_function_analysis(regions):
	bis_func_counts = get_business_function_counts(regions)
	business_functions = get_business_functions(regions)
	return business_functions, bis_func_counts

def get_event_analysis(regions):
	return get_site_events(regions)

def get_site_access_analysis(regions):
	return get_total_site_access(regions)

def get_owned_status_analysis(regions):
	return get_num_owned(regions)

def get_bis_cc_analysis(regions):
	bcct = get_bis_cc_type(regions)
	bcct_connect = get_connectivity_type_given_bis_cc_type(regions)
	return bcct, bcct_connect

def get_lead_agency_analysis(regions):
	agency_per_type = get_agency_per_type(regions)
	agency_per_type = sort_map(agency_per_type)
	return cc_types_extended, agency_per_type

def get_tele_core_analysis(regions):
	tele_core = get_tele_core_data(regions)
	bis_tele_core = get_bis_tele_core_data(regions)
	cc_tele_core = get_cc_tele_core_data(regions)
	avg_tele_core_users = get_tele_core_users(regions)
	return tele_core, bis_tele_core, cc_tele_core, avg_tele_core_users
	
def get_poe_capability_analysis(regions):
	return get_poe(regions)
