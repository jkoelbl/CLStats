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
		return self.agent_type + ',' + \
			self.complexity + ',' + \
			self.reporting
			

class platform_details:
	def __init__(self, data):
		self.platform = data[0]
		self.contractors = [data[1], data[3], data[5]]
		self.staff = [data[2], data[4], data[6]]
		self.total = sum(self.contractors) + sum(self.staff)
		if self.contractors == self.staff and self.staff == [0,0,0]:
			self.platform == ''

	def __str__(self):
		temp = self.platform
		for c in self.contractors:
			temp += ',' + str(c)
		for s in self.staff:
			temp += ',' + str(s)
		temp += ',' + str(self.total)
		return temp

def is_zero(list):
	for item in list:
		if item:
			return False
	return True

class program:
	def __init__(self, data):
		self.agency = data[0]
		self.name = data[1]
		self.is_247 = (data[2] == '24/7')
		self.bis_func = self.get_bis_func(data[3:14])
		self.events = data[14]
		self.telephony_users = platform_details(data[15:22])
		self.contact_center = platform_details(data[22:29])	#24-31
		self.cc_complexity = cc_complexity(data[29:32])		#32-35
		self.reporting = data[32]							#35
		if data[22:29] == [0,0,0,0,0,0]:					#25-31
			self.cc_complexity = cc_complexity(['','',''])

	def get_bis_func(self, data):
		list = [True for _ in data]
		for i in range(len(data)):
			list[i] = (data[i] == 'yes')
		return list
	
	def __str__(self):
		temp = str(self.name) + ',' + str(self.agency)
		temp += ',' + str(self.is_247)
		temp += ',' + str(self.events)
		temp += '\n    '
		for i in range(len(self.bis_func)):
			if i:	temp += ','
			temp += str(self.bis_func[i])
		temp += '\n    ' + str(self.telephony_users)
		temp += '\n    ' + str(self.contact_center)
		temp += '\n    ' + str(self.cc_complexity)
		temp += '\n    ' + str(self.reporting)
		return temp


class site:
	def __init__(self, data):
		self.id = data[0]
		self.addr = data[1]
		self.avaya_type = data[2] if data[2] else ''
		self.region = data[5]
		self.lead_agency = data[6]
		self.total = 0
		
		data[3] = data[3].strip()
		if not data[3]:	data[3] = 'none'
		self.is_leased = data[3]
		
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
		temp = str(self.id)
		temp += ',' + str(self.is_leased)
		temp += ',' + str(self.region)
		temp += ',' + str(self.lead_agency)
		temp += ',' + str(self.total)
		temp += ',' + str(self.site_size)
		for program in self.programs:
			temp += '\n  ' + str(program)
		return temp + '\n'
