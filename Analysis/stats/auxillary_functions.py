comp = ('basic', 'advanced')

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
