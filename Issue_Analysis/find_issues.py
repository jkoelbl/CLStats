TEMPLATE = 'sample_issues.txt'

def load_possible_issues():
	with open(TEMPLATE, newline='') as file:
		reader = csv.reader(file, delimiter=',', quotechar='\"')
		return [row for row in reader]

def get_issues(survey):
	pass