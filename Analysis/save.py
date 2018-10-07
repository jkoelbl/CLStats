def encode_list(list, include_sum=True):
	temp = [str(s) for s in list]
	if include_sum:
		return ','.join(temp)+','+str(sum(list))
	return ','.join(temp)
	
def encode_maplist(maplist, include_sum=True):
	temp = {str(k):v for k,v in maplist.items()}
	s, first = '', True
	for k,v in temp.items():
		if not first:	s += '\n'
		s += k+','+encode_list(v, include_sum)
		first = False
	return s

def encode_multilist(multilist, include_sum=True):
	temp = {i:multilist[i] for i in range(len(multilist))}
	if include_sum:
		return encode_maplist_w_sum(temp, include_sum)
	return encode_maplist(temp, include_sum)

def encode_maplist_w_sum(maplist, include_sum=True):
	s = encode_maplist(maplist, include_sum)
	length = [len(v) for v in maplist.values()][0]
	if include_sum:
		sumlist = {'Total':[0 for _ in range(length)]}
		for v in maplist.values():
			for i in range(len(v)):
				sumlist['Total'][i] += v[i]
		s += '\n'+encode_maplist(sumlist, include_sum)
	return s

def encode_multimap(map_multilist, include_sum=True):
	temp, first = '', True
	for k,v in map_multilist.items():
		if not first:	temp += '\n'
		temp += str(k)+'\n'+encode_maplist(v, include_sum)
		first = False
	return temp

def init_outfile():
	temp = 'Analysis of Site Survey Data'
	temp += '\n,Site Sizes'
	temp += '\n,<11 Workers,11-25 Workers,26-50 Workers,51-100 Workers,101-250 Workers,251-500 Workers,>500 Workers,Total'
	return temp

def add_new_data(str, title='', newline=True):
	temp = ''
	if newline:	temp += '\n'
	if title:	temp += '\n'+title+''
	temp += '\n'+str
	return temp
