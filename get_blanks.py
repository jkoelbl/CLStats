from Common.formatting import *

PATH = 'C:\\Users\\acesp\\Desktop\\Site Survey Responses\\CSVs\\Site Summary 100418 v4.csv'

sites = load_data(PATH)
for i in range(len(sites)):
	if not sites[i][0] and not sites[i][1]:
		print(sites[i])