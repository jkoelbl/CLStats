comp = ('basic', 'advanced')
moreton = ('moreton core','remote moreton','moreton')
winters = ('winters core','remote winters','winters')

def get_tele_core(site):
	if site.avaya_type in moreton:
		return 'moreton'
	if site.avaya_type in winters:
		return 'winters'
	return ''

def sort_map(map):
	return {item:map[item] for item in sorted([k for k in map.keys()])}

def get_option(site, data_type, none_multi, optional_condition='True'):
	command = 'program.'+data_type
	selection_map, selected = {}, ''
	for program in site.programs:
		if eval(command) and eval(optional_condition):
			selected = eval(command)
			selection_map[selected] = None
	if not len(selection_map):	return none_multi[0]
	if len(selection_map) > 1:	return none_multi[1]
	return selected

def get_bis_platform(site):
	return get_option(site, \
					'telephony_users.platform', \
					('none', 'both'))

def get_cc_platform(site):
	return get_option(site, \
					'contact_center.platform', \
					('none', 'both'), \
					'program.cc_complexity.complexity in comp' + \
					' and program.contact_center.total')

def get_site_access(site):
	return get_option(site, \
					'reporting', \
					('none', 'multiple'))

def get_event(site):
	return get_option(site, \
					'events', \
					('none', 'multiple'))

def determine_platform_combination(site):
	platform = {'cisco':'C', 'avaya':'A', 'both':'C/A', 'none':''}
	tele = platform[get_bis_platform(site)]
	cc = platform[get_cc_platform(site)]
	if not tele and not cc:	return ''
	elif not tele:	return cc+'cc'
	elif not cc:	return tele
	return tele+'+'+cc+'cc'

def get_program_bis_platform_total(program):
	type = program.telephony_users.platform
	if not type:	type = 'none'
	total = program.telephony_users.total
	return type, total

def get_program_cc_platform_total(program):
	type = program.contact_center.platform
	if not type:	type = 'none'
	total = 0
	if program.cc_complexity.complexity in comp and program.contact_center.total:
		total = program.contact_center.total
	return type, total

def get_users_agents(site):
	users, agents = 0, 0
	for program in site.programs:
		users += program.telephony_users.total
		agents += program.contact_center.total
	return users, agents
