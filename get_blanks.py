from Analysis.formatting import *

PATH = 'C:\\Users\\acesp\\Desktop\\Site Survey Responses\\CSVs\\Site Summary 100418 v4.csv'

sites = load_data(PATH)
for site in sites:
	if str(site.total) == '6':
		print(site.id, site.addr)