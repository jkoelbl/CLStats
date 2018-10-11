import sys,os
from .classes import site
from .find_issues import get_issues, load_possible_issues

OUTPUT = 'Results - Issues.csv'

def get_folders():
	prev = os.getcwd()
	os.chdir('..')
	folders = (os.getcwd()+'/'+path for path in sys.argv[1:])
	os.chdir(prev)
	return folders

def get_files(folders):
	files = {folder:[] for folder in folders}
	for folder in folders:
		for item in os.listdir(folder):
			path = folder+'/'+item
			if not os.path.isdir(path) and item[:2] != '~$' and item.split('.')[-1] == 'xlsx':
				files[folder].append(path)
	return files

def load_data_from_file(file):
	wb = openpyxl.load_workbook(filename=path, read_only=True, data_only=True)
	if not wb['Site Info']['E3'].value:	# is old survey
		return site_old(wb)
	if wb['Site Info']['G45'].value: # is sh/sslc survey
		return site_sh(wb)
	return site_new(wb)	# is current survey

def write_to_output(issues, folders):
	with open(OUTPUT, 'w') as output:
		output.truncate(0)
		for i in range(len(folders)):
			if i:	output.write('\n')
			output.write(sys.argv[i+1]+'\n')
			for issue in issues[folders[i]]:
				output.write(issue+'\n')

def get_issues():
	folders = get_folders()
	files = get_files(folders)
	surveys = {folder:[load_data_from_file(file) for file in files[folder]] for folder in folders}
	issues = {folder:[find_issues(survey) for survey in surveys[folder]] for folder in folders}
	write_to_output(issues, folders)
	print('0')

if __name__ == '__main__':
	get_issues()
