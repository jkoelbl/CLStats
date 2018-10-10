from time import sleep

IN = 'Issues.csv'
map = {}

with open(IN) as file:
	file.readline()
	for line in file:
		data, i = line[6:], int(line[0:4])
		if i not in map:	map[i] = []
		map[i].append(data)
	
	print('Total number of issues:', sum([len(v) for v in map.values()]))
	print('Total number of items affected:', len(map))
	print('Maximum number of issues:', max([len(v) for v in map.values()]))
	print('Average number of issues:', sum([len(v) for v in map.values()])/len(map), end='\n\n')
	print('Distribution of number of issues:')
	
	dist = [0 for _ in range(10)]
	for v in map.values():	dist[len(v)]+=1
	[print(i, ':', dist[i]) for i in range(len(dist))]
	print()
	
	dupes = 0
	for k in map.keys():
		for m in map[k]:
			if m[:6] == ',,\"Dup':
				dupes += 1
	print('Duplicates/potential duplicates:', dupes, end='\n\n')
	
	issues = {}
	for v in map.values():
		for e in v:
			e = e.strip('\n').split(',')[-1]
			if e not in issues:
				issues[e] = 1
			else:	issues[e] += 1
	print('Common issues:')
	[print(v, ':', k) for k,v in issues.items()]
