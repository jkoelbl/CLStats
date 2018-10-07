from .auxillary_functions import *

complexity_types_extended = ('Basic/Advanced', 'Low Only', 'None')
response_types_extended = ('Lobby Area', \
						'Customer Facing Location', \
						'Back Office Support Staff', \
						'IT Staff', \
						'Machine/Print/Sign Shop', \
						'Contact/Call Center', \
						'Training Location', \
						'Public Hearing/Meeting Rooms', \
						'Closed Location', \
						'Warehouse/Storage', \
						'Shared Operator Access with Multiple Sites')

def get_complexity(site_complexities, site):
	temp, comp = {}, ''
	for program in site.programs:
		if program.cc_complexity.complexity:
			comp = program.cc_complexity.complexity
			temp[comp] = None
	if not len(temp):	return 'None'
	if 'advanced' in temp or 'basic' in temp:	return 'Basic/Advanced'
	return 'Low Only'
	
def get_site_complexities(sites):
	site_complexities = {type:[0 for _ in range(7)] for type in complexity_types_extended}
	for site in sites:
		complexity = get_complexity(site_complexities, site)
		site_complexities[complexity][site.site_size] += 1
	return site_complexities

def get_business_functions(sites):
	business_functions = {type:[[0 for _ in range(7)] for _ in range(11)] for type in ('Yes', 'No')}
	for site in sites:
		temp_responses = ['No' for _ in range(11)]
		for program in site.programs:
			for i in range(11):
				if program.bis_func[i]:
					temp_responses[i] = 'Yes'
		for i in range(11):
			response = temp_responses[i]
			business_functions[response][i][site.site_size] += 1
	
	business_functions = {bf:{response_types_extended[i]:val[i] for i in range(len(val))} for bf,val in business_functions.items()}
	return business_functions

def get_bf_count(site):
	bf = [0 for _ in range(11)]
	for program in site.programs:
		for i in range(11):
			if program.bis_func[i]:
				bf[i] = 1
	return sum(bf)
	
def get_business_function_counts(sites):
	bfc = [[0 for _ in range(7)] for _ in range(12)]
	for site in sites:
		count = get_bf_count(site)
		bfc[count][site.site_size] += 1
	return bfc
