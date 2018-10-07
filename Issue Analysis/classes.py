class site:
	def __init__(self, wb, commands, detections):
		ws = wb['Site Info']
		self.id = ws[commands[0]].value
		self.addr = ws[commands[1]].value
		self.region = ws[commands[2]].value
		self.lead_agency = ws[commands[3]].value
		self.total_programs = 0
		self.programs = []
		self.add_programs(wb, commands[4:], detections)
	
	def add_programs(self, wb, commands, detections):
		programs = []
		for i in range(8):
			sheet = wb.sheetnames[i+1]
			if wb['Site Info'][detections[i]].value:
				programs.append(sheet)
		self.programs = [program(wb[p], commands) for p in programs]
		self.total_programs = len(programs)


class program:
	def __init__(self, ws):
		self.name = ws[commands[0]].value
		self.agency = ws[commands[1]].value
		self.agency_other = ws[commands[2]].value
		self.operations = [ws[command].value for command in commands[3:17]]
		self.contingencies = [ws[command].value for command in commands[17:20]]
		self.business_functions = [ws[command].value for command in commands[20:31]]
		self.connectivity = [ws[command].value for command in commands[31:32]]
		self.telephony_platform = ws[commands[33]].value
		self.tele_users = [ws[command] for command in commands[34]]
		self.cc_platform = ws[commands[35]].value
		self.agent_types = ws[commands[36]].value
		self.agents = [ws[command] for command in commands[37]]
		self.complexity = [ws[command] for command in commands[38:42]]
		self.reporting = [ws[command] for command in commands[42:46]]
		
OLD = ('E32','C5','E30','C25','C5','C6','D6', \
		'C13','C14','C15','C16','C17','C18','C19', \
		'E13','E14','E15','E16','E17','E18','E19', \
		'K24','K25','K26', \
		'E36','E37','E38','E39','E40','E41','E42','E43','E44','E45','E46', \
		'I37','K37','D55', \
		('E61','F61','H61','E62','F62','H62','E62','F62','H62'), \
		'D68','E84', \
		('E74','F74','H74','E75','F75','H75','E76','F76','H76'), \
		'E80','E79','E78','E81','K82','K83','K80','K81')
NEW = ('E3','C9','E5','E4','C5','C6','D6', \
		'C13','C14','C15','C16','C17','C18','C19', \
		'E13','E14','E15','E16','E17','E18','E19', \
		'E24','E25','E26', \
		'E30','E31','E32','E33','E34','E35','E36','E37','E38','E39','E40', \
		'I31','K31','D49', \
		('C56','D56','C57','D57','C58','D58'), \
		'D63','E66', \
		('C72','D72','C73','D73','C74','D74'), \
		'E78','E77','E75','E79','K79','K80','K77','K78')
SH = ('E3','C9','E5','E4','C5','C6','D6', \
		'C13','C14','C15','C16','C17','C18','C19', \
		'E13','E14','E15','E16','E17','E18','E19', \
		'E24','E25','E26', \
		'E30','E31','E32','E33','E34','E35','E36','E37','E38','E39','E40', \
		'I31','K31','D73', \
		('C80','D80','C81','D81','C82','D82'), \
		'D87','E90', \
		('C96','D96','C97','D97','C98','D98'), \
		'E102','E101','E100','E103','E103','E104','E101','E102')
DETECTION_OLD = ('C16','C17','C18','C19','C20','C21','C22','C23')
DETECTION_NEW = ('B21','B22','B23','B24','B25','B26','B27','B28')

class site_old(site):
	def __init__(self, wb):
		site.__init__(self, wb, OLD, DETECTION_OLD)

class site_new(site):
	def __init__(self, wb):
		site.__init__(self, wb, NEW, DETECTION_NEW)

class site_sh(site):
	def __init__(self, wb):
		site.__init__(self, wb, SH, DETECTION_NEW)
