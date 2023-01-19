import json
import random

pre_path = 'anno.json'
nex_path = 'rel.json'
data = [] 

# PER LOC ORG

rel_json = {
	'PER':{
		'PER':'Married',
		'LOC':'Lived',
		'ORG':'Worked'
	},
	'LOC':{
		'PER':'Lived',
		# 'LOC':'',
		'ORG':'Placed'
	},
	'ORG':{
		'PER':'Worked',
		'LOC':'Placed',
		# 'ORG':''
	}
}

def rand(percent):
	return random.uniform(0, 1) < percent

with open(pre_path, 'r', encoding='utf-8') as f:
	source = json.load(f)

for item in source:
	buff = {}
	buff['sen'] = item['sen']
	buff['nodes'] = item['tag']

	rel = []
	len_node = len(buff['nodes'])
	for index_1 in range(len_node-1):
		for index_2 in range(index_1+1, len_node):
			node_1 = buff['nodes'][index_1]; node_2 = buff['nodes'][index_2]
			try:
				rel_type = rel_json[node_1['type']][node_2['type']]
			except:
				continue
			if rand(0.3):
				rel.append({
					'node_1': index_1,
					'node_2': index_2,
					'type': rel_type
				})
				continue
	if(len(rel)>0):
		buff['relation'] = rel
	data.append(buff)

with open(nex_path, 'w', encoding='utf-8') as f:
	json.dump(data, f, indent=4, ensure_ascii=False)


