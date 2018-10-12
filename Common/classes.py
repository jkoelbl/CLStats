"""
notes:
	data are encoded as follows:
		business functions:
			'yes' = True, otherwise False
		Site Sizes:
			<11 = 0
			11-25 = 1
			26-50 = 2
			51-100 = 3
			101-250 = 4
			251-500 = 5
			>500 = 6
		Staff/Contractor roles (indeces):
			0 = onsite
			1 = mobile
			2 = telecommuting
"""

class cc_complexity:
	def __init__(self, data):
		self.agent_type = data[0]
		self.complexity = data[1]
		self.reporting = data[2]

	def __str__(self):
		group = [self.agent_type, self.complexity, self.reporting]
		return ','.join([str(g) for g in group])
			

class platform_details:
	def __init__(self, data):
		self.platform = data[0]
		self.contractors = [data[1], data[3], data[5]]
		self.staff = [data[2], data[4], data[6]]
		self.total = data[7]
		if not self.total:
			self.total = sum(self.contractors+self.staff)

	def __str__(self):
		group = [self.platform]+self.contractors+self.staff+[self.total]
		return ','.join([str(g) for g in group])

def is_zero(list):
	return sum([1 for e in list if e])

class program:
	def __init__(self, data):
		self.agency = data[0]
		self.name = data[1]
		self.is_247 = (data[2] == '24/7')
		self.bis_func = self.get_bis_func(data[3:14])
		self.events = data[14]
		self.telephony_users = platform_details(data[15:23])
		self.contact_center = platform_details(data[24:32])
		self.cc_complexity = cc_complexity(data[32:35])
		self.reporting = data[35]
		"""if data[25:32] == [0,0,0,0,0,0,0] and not self.bis_func[5]:
			self.platform = ''
			self.cc_complexity = cc_complexity(['','',''])
"""
	def get_bis_func(self, data):
		return [e == 'yes' for e in data]
	
	def __str__(self):
		group = [self.name, self.agency, self.is_247, events]
		group2 = [','.join(self.bis_func), self.telephony_users, self.contact_center, self.cc_complexity, self.reporting]
		return ','.join([str(g) for g in group]) + \
				'\n    '.join([str(g) for g in group])


class site:
	def __init__(self, data):
		self.id = data[0]
		self.addr = data[1]
		self.avaya_type = data[2] if data[2] else ''
		self.region = data[5]
		self.lead_agency = data[6]
		self.total = 0
		self.is_leased = data[3] if data[3] else 'none'
		self.programs = []
		self.site_size = 0

	def get_site_size(self):
		if self.total <= 10:	return 0
		elif self.total <= 25:	return 1
		elif self.total <= 50:	return 2
		elif self.total <= 100:	return 3
		elif self.total <= 250:	return 4
		elif self.total <= 500:	return 5
		return 6

	def new_program(self, data):
		self.programs.append(program(data[7:]))
		self.total += self.programs[-1].telephony_users.total
		self.total += self.programs[-1].contact_center.total
		self.site_size = self.get_site_size()

	def __str__(self):
		group = (self.id, self.addr, self.avaya_type, \
				self.is_leased, self.region, self.lead_agency, \
				self.total, self.site_size)
		group2 = [''] + self.programs
		return ','.join([str(g) for g in group]) + \
				'\n '.join([str(g) for g in group2])+'\n'
