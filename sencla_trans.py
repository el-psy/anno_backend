import json

pre_path = 'anno.json'
nex_path = 'sencla.json'
data = [] 

with open(pre_path, 'r', encoding='utf-8') as f:
	buff = json.load(f)

for item in buff:
	if len(item['tag'])>0:
		item['tag'] = item['tag'][0]['type']
	else:
		del(item['tag'])
	data.append(item)

with open(nex_path, 'w', encoding='utf-8') as f:
	json.dump(buff, f, indent=4, ensure_ascii=False)
# print(buff[1])