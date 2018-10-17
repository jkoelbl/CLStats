import sys
from Major_Functionality import *

commands = {item:None for item in sys.argv[1:]}
if not len(commands):
	site_analysis()
	user_summary()
else:
	if "site" in commands:
		site_analysis()
	if "harvest" in commands:
		get_all_data()
	if "user" in commands:
		get_all_data()
	"""if "issues" in commands:
		get_issues()"""
