def modify(x):
	if not x or str(x).lower()=='select' or str(x).lower()=='no':
		return ''
	return str(x)

class site:
	def __init__(self, wb, commands, detections):
		ws = wb['Site Info']
		self.id = modify(ws[commands[0]].value)
		self.addr = modify(ws[commands[1]].value)
		self.region = modify(ws[commands[2]].value)
		self.lead_agency = modify(ws[commands[3]].value)
		self.programs = []
		self.add_programs(wb, commands[4:], detections)
	
	def add_programs(self, wb, commands, detections):
		programs = []
		for i in range(len(detections)):
			sheet = wb.sheetnames[i+1]
			detect = wb['Site Info'][detections[i]].value
			if not detect or not str(detect).strip():
				break
			programs.append(sheet)
		self.programs = [program(wb[p], commands) for p in programs]
	
	def __str__(self):
		group = (self.id,'\"'+self.addr+'\"','','','',self.region,self.lead_agency)
		temp = ','.join(group)
		for i in range(len(self.programs)):
			if i:	temp += '\n' + ','.join(['' for _ in group])
			temp += ',' + str(self.programs[i])
		return temp+'\n'


class program:
	def __init__(self, ws, commands):
		self.name = modify(ws[commands[0]].value)
		self.agency = modify(ws[commands[1]].value)
		if ws[commands[1]].value == 'Other:' and modify(ws[commands[2]].value):
			self.agency = modify(ws[commands[2]].value)
		self.operations = self.get_operations(ws, commands[3:17])
		self.contingencies = self.get_contingencies(ws, commands[17:20])
		self.business_functions = [modify(ws[command].value) for command in commands[20:31]]
		self.connectivity = [modify(ws[command].value) for command in commands[31:33]]
		self.telephony_platform = modify(ws[commands[33]].value)
		self.tele_users = [modify(ws[command].value) for command in commands[34]]
		self.cc_platform = modify(ws[commands[35]].value)
		self.agent_types = modify(ws[commands[36]].value)
		self.agents = [modify(ws[command].value) for command in commands[37]]
		self.complexity = self.get_complexity(ws, commands[38:42])
		self.reporting = self.get_reporting(ws, commands[42:46])
	
	def get_operations(self, ws, list):
		list = [str(ws[item].value).lower() for item in list]
		for i in range(7):
			if list[i] == 'closed' or list[i] != list[i+7]:
				return 'Day'
		return '24/7'
	
	def get_contingencies(self, ws, list):
		list = [str(ws[item].value).lower() for item in list]
		selects = sum([1 for item in list if item=='select'])
		yeses = sum([1 for item in list if item=='yes'])
		noes = sum([1 for item in list if item=='no'])
		if noes == 3:	return 'None'
		if yeses > 1:	return 'Multiple'
		if selects > 1:	return ''
		if selects == 1 and noes == 1:	return ''
		types = ('Offsite','Recording','Redirected')
		for i in range(len(list)):
			if list[i]=='yes':
				return types[i]
		return 'None'
		
	def get_complexity(self, ws, list):
		list = [str(ws[item].value).lower() for item in list]
		if 'select' == list[2]:	return ''
		if 'yes' == list[2]:	return 'Advanced'
		if 'select' == list[1]:	return ''
		if 'yes' == list[1]:	return 'Basic'
		if 'select' in list:	return ''
		if 'yes' in list:		return 'Low'
		return 'None'
	
	def get_reporting(self, ws, list):
		list = [str(ws[item].value).lower() for item in list]
		if 'select' in list[2:4]:	return ''
		if 'yes' in list[2:4]:	return 'Advanced'
		if 'select' in list[:2]:	return ''
		if 'yes' in list[:2]:	return 'Standard'
		return 'None'
	
	def __str__(self):
		group = (self.agency, '\"'+self.name+'\"', self.operations, \
				','.join(self.business_functions), self.contingencies, \
				self.telephony_platform, ','.join(self.tele_users), \
				self.cc_platform, ','.join(self.agents), \
				self.agent_types, self.complexity, self.reporting, \
				','.join(self.connectivity))
		return ','.join(group)

		
OLD = ('E32','C5','E30','C25','C5','C6','D6', \
		'C13','C14','C15','C16','C17','C18','C19', \
		'E13','E14','E15','E16','E17','E18','E19', \
		'K24','K25','K26', \
		'E36','E37','E38','E39','E40','E41','E42','E43','E44','E45','E46', \
		'I37','K37','D55', \
		('E61','F61','H61','E63','F63','H63','E62','F62','H62'), \
		'D68','E84', \
		('E74','F74','H74','E76','F76','H76','E75','F75','H75'), \
		'E80','E79','E78','E81','K82','K83','K80','K81')
NEW = ('E3','C9','E5','E4','C5','C6','D6', \
		'C13','C14','C15','C16','C17','C18','C19', \
		'E13','E14','E15','E16','E17','E18','E19', \
		'E24','E25','E26', \
		'E30','E31','E32','E33','E34','E35','E36','E37','E38','E39','E40', \
		'I31','K31','D49', \
		('C56','D56','C58','D58','C57','D57'), \
		'D63','E66', \
		('C72','D72','C74','D74','C73','D73'), \
		'E78','E77','E75','E79','K79','K80','K77','K78')
SH = ('E3','C9','E5','E4','C5','C6','D6', \
		'C13','C14','C15','C16','C17','C18','C19', \
		'E13','E14','E15','E16','E17','E18','E19', \
		'E24','E25','E26', \
		'E30','E31','E32','E33','E34','E35','E36','E37','E38','E39','E40', \
		'I31','K31','D73', \
		('C80','D80','C82','D82','C81','D81'), \
		'D87','E90', \
		('C96','D96','C98','D98','C97','D97'), \
		'E102','E101','E100','E103','E103','E104','E101','E102')
DETECTION_OLD = ('C16','C17','C18','C19','C20','C21','C22','C23')
DETECTION_NEW = ('B21','B22','B23','B24','B25','B26','B27','B28','B29','B30','B31','B32')

class site_old(site):
	def __init__(self, wb):
		super().__init__(wb, OLD, DETECTION_OLD)

class site_new(site):
	def __init__(self, wb):
		super().__init__(wb, NEW, DETECTION_NEW)

class site_sh(site):
	def __init__(self, wb):
		super().__init__(wb, SH, DETECTION_NEW)
