from .auxillary_functions import *

cs_types = ('contractors', 'staff')

def get_platform_users(sites, get_program_platform_total):
	types = ('cisco','avaya','none')
	users = {type:[0 for _ in range(7)] for type in types}
	comp = ('basic','advanced')
	for site in sites:
		for program in site.programs:
			type, total = get_program_platform_total(program)
			users[type][site.site_size] += total
	types_extended = ('Cisco','Avaya','None')
	users = {types_extended[i]:users[types[i]] for i in range(len(types))}
	return users

def get_total_users(sites):
	total_users = [{k:[0 for _ in range(3)] for k in cs_types} for _ in range(7)]
	for site in sites:
		for program in site.programs:
			for i in range(3):
				total_users[site.site_size]['contractors'][i] += program.telephony_users.contractors[i]
				total_users[site.site_size]['contractors'][i] += program.contact_center.contractors[i]
				total_users[site.site_size]['staff'][i] += program.telephony_users.staff[i]
				total_users[site.site_size]['staff'][i] += program.contact_center.staff[i]
	return total_users

def avg_contractors_staff(total_users, site_sizes):
	cs = [[0 for _ in range(7)], [0 for _ in range(7)]]
	for i in range(len(total_users)):
		for k in range(2):
			cs[k][i] = round(sum(total_users[i][cs_types[k]])/site_sizes[i], 1)
	return {'Contractors':cs[0], 'Staff':cs[1]}

def get_total_user_types(total_users):
	user_types = ('Onsite','Mobile','Telecommuters')
	user_total = [[0 for _ in range(7)] for _ in range(3)]
	for i in range(3):
		for j in range(len(total_users)):
			user_total[i][j] += total_users[j][cs_types[0]][i]
			user_total[i][j] += total_users[j][cs_types[1]][i]
	return {user_types[i]:user_total[i] for i in range(len(user_types))}

def avg_user_types(total_users, site_sizes):
	user_types = ('Onsite','Mobile','Telecommuters')
	user_avg = get_total_user_types(total_users)
	user_avg = [v for v in user_avg.values()]
	for i in range(3):
		for j in range(len(total_users)):
			user_avg[i][j] = round(user_avg[i][j]/site_sizes[i], 1)
	return {user_types[i]:user_avg[i] for i in range(len(user_types))}

def get_total_users_agents_at_site(site):
	return sum([program.telephony_users.total for program in site.programs]), \
			sum([program.contact_center.total for program in site.programs])

def get_avg_users_at_avaya(sites):
	user_types = ('Business Telephony Users','Contact Center Agents')
	data = {type:[0 for _ in range(7)] for type in user_types}
	total_sites = [0 for _ in range(7)]
	for site in sites:
		combo = determine_platform_combination(site)
		if combo == 'A+Acc':
			total_sites[site.site_size] += 1
			users, agents = get_total_users_agents_at_site(site)
			data['Business Telephony Users'][site.site_size] += users
			data['Contact Center Agents'][site.site_size] += agents
	for k in data.keys():
		for i in range(7):
			data[k][i] = round(data[k][i]/total_sites[i], 1)
	return data
