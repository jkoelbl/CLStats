class site_sh:
	def __init__(self, wb):
		ws = wb['Site Info']
		self.id = ws['E3'].value
		self.addr = '\"'+ws['C8'].value+'\"'
		self.region = ws['E5'].value
		self.lead_agency = ws['E4'].value
		self.total_programs = 0
		self.programs = []
		self.add_programs(wb)
	
	def add_programs(self, wb):
		programs = []
		for i in range(21,29):
			sheet = wb.sheetnames[i-20]
			if wb['Site Info']['B'+str(i)].value:
				print(sheet)
				programs.append(sheet)
			else:	break
		for program in programs:
			self.add_program(wb[program])

	def add_program(self, ws):
		self.programs.append(program_sh(ws))
		self.total_programs += 1
	
	def __str__(self):
		group = (str(self.id), self.addr, '', '', \
				str(self.region), str(self.lead_agency))
		temp = ','.join(group)+','+str(self.programs[0])
		for i in range(1, len(self.programs)):
			temp += '\n'+','.join(['' for _ in group])+','+str(self.programs[i])
		return temp


def add_element(cell):
	if not cell.value:	return ''
	if str(cell.value).lower() == 'no':	return ''
	if str(cell.value).lower() == 'select':	return ''
	return cell.value


class program_sh:
	def __init__(self, ws):
		self.name = ws['C5'].value
		self.agency = ws['C6'].value
		if ws['C6'].value == 'Other:':
			self.agency = add_element(ws['D6'])
		self.operations = self.get_operations(ws)
		self.contingencies = self.get_contingencies(ws)
		self.business_functions = self.get_bis_func(ws)
		self.connectivity = [add_element(ws['I31']), add_element(ws['K31'])]
		self.telephony_platform = add_element(ws['D73'])
		self.tele_users = self.get_users(ws, 80)
		self.cc_platform = add_element(ws['D87'])
		self.agent_types = add_element(ws['E90'])
		self.agents = self.get_users(ws, 96)
		self.complexity = self.get_complexity(ws)
		self.reporting = self.get_reporting(ws)
	
	def get_operations(self, ws):
		for i in range(13,20):
			if ws['C'+str(i)].value != ws['E'+str(i)].value:
				return 'Day'
		return '24/7'
	
	def get_contingencies(self, ws):
		types = ('Offsite', 'Recording', 'Redirected')
		list = [ws['E'+str(i)].value.lower() for i in range(24,27)]
		selects = sum([1 if list[i]=='select' else 0 for i in range(len(list))])
		yeses = sum([1 if list[i]=='yes' else 0 for i in range(len(list))])
		noes = sum([1 if list[i]=='no' else 0 for i in range(len(list))])
		if selects > 1:	return ''
		if selects == 1 and yeses < 2:	return ''
		if yeses > 1:	return 'Multiple'
		if noes == 3:	return 'None'
		for i in range(3):
			if list[i] == 'yes':
				return types[i]
	
	def get_bis_func(self, ws):
		bf = ['' for _ in range(11)]
		for i in range(30,41):
			if ws['E'+str(i)].value.lower() == 'yes':
				bf[i-30] = 'Yes'
		return bf
	
	def get_users(self, ws, shift):
		temp = [['C'+str(i),'D'+str(i)] for i in range(shift,3+shift)]
		strs = []
		for i in range(3):
			strs += temp[i]
		list = [str(ws[strs[i]].value) for i in range(len(strs))]
		list = [elem if elem else '0' for elem in list]
		
		bad_insert = False
		for i in range(len(list)):
			try:
				if not int(list[i]):	list[i] = ''
			except ValueError:
				bad_insert = True
				break
		if bad_insert:	list = ['' for _ in list]
		return list
	
	def get_complexity(self, ws):
		answers = (add_element(ws['E102']).lower(), \
					add_element(ws['E101']).lower(), \
					add_element(ws['E100']).lower(), \
					add_element(ws['E103']).lower())
		if not answers[0]:	return ''
		if answers[0] == 'yes':	return 'Advanced'
		if not answers[1]:	return ''
		if answers[1] == 'yes':	return 'Basic'
		if not answers[2] or not answers[3]:	return ''
		if answers[2] == 'yes' or answers[3] == 'yes':	return 'Low'
		return ''
	
	def get_reporting(self, ws):
		answers = (add_element(ws['K103']).lower(), \
					add_element(ws['K104']).lower(), \
					add_element(ws['K101']).lower(), \
					add_element(ws['K102']).lower())
		if not self.complexity:	return ''
		if not answers[0] and not answers[1]:	return ''
		if answers[0] == 'yes' or answers[1] == 'yes':	return 'Advanced'
		if not answers[2] and not answers[3]:	return ''
		if answers[2] == 'yes' or answers[3] == 'yes':	return 'Standard'
		return 'None'
	
	def __str__(self):
		group = [self.agency, '\"'+self.name+'\"', self.operations, \
				','.join(self.business_functions), \
				self.contingencies, self.telephony_platform, \
				','.join(self.tele_users), \
				'', '', self.cc_platform, \
				','.join(self.agents), \
				'', self.agent_types, \
				self.complexity, self.reporting, self.connectivity[0], self.connectivity[1]]
		group = [str(g) for g in group]
		return ','.join(group)
