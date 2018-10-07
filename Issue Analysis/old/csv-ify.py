IN = 'Issues.txt'
OUT = 'Issues.csv'

def get_input():
	with open(IN) as file:
		return [line.strip('\n') for line in file]

def process_input(raw):
	temp = [x.split('\t') for x in raw]
	out = [[x[0]] for x in temp]
	for i in range(len(out)):
		t = temp[i][1].split(': ')
		if len(t) == 1:
			t = [''] + t
		elif len(t) == 3:
			t[1] += ': ' + t[2]
			del t[2]
		out[i] += t
	return out

def refine_input(proc):
	for i in range(len(proc)):
		if not proc[i][0]:
			proc[i][0] = proc[i-1][0]
		else:
			proc[i][0] = int(proc[i][0].strip(' -'))
		if proc[i][1][:8] == 'Program ':
			proc[i][1] = int(proc[i][1].strip('Program '))
	return proc

def format_csv(proc):
	csv = ['' for _ in proc]
	for i in range(len(proc)):
		for j in range(len(proc[i])):
			if j:
				csv[i] += ','
			if proc[i][j]:
				csv[i] += '\"'+str(proc[i][j])+'\"'
	return csv

def write_to_file():
	proc = get_input()
	proc = process_input(proc)
	proc = refine_input(proc)
	proc = format_csv(proc)
	with open(OUT, 'w') as file:
		file.truncate(0)
		file.write('Facility ID,Program,Issue')
		for p in proc:
			file.write('\n'+p)
	return proc

[print(p) for p in write_to_file()]
