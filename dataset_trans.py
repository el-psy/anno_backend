import json

pre_path = './msra_test_bio'
nex_path = 'anno.json'
data = [] 

with open(pre_path, 'r', encoding='utf-8') as f:
	buff = {
		'sen':'',
		'tag':[]
	}
	tag_type = ''
	start = 0; end = 0

	# point = 0
	for line in f.readlines():
		line_buff = line.replace('\n', '').split('	')
		# print(len(line_buff))
		# point +=1
		# if(point>100): break
		if len(line_buff) == 1:
			data.append(buff)
			buff = {
				'sen':'',
				'tag':[]
			}
		elif len(line_buff) == 2:
			buff['sen'] = buff['sen'] + line_buff[0]
			tag = line_buff[1].split('-')
			# print(tag)
			if tag[0] == 'O':
				if tag_type != '':
					end = len(buff['sen'])-1
					buff['tag'].append({
						'type': tag_type,
						'start': start,
						'end': end
					})
					tag_type = ''
			elif tag[0] == 'B':
				if tag_type != '':
					end = len(buff['sen'])-1
					buff['tag'].append({
						'type': tag_type,
						'start': start,
						'end': end
					})
				tag_type = tag[1]
				start = len(buff['sen'])-1
			elif tag[0] == 'I':
				pass


with open(nex_path, 'w', encoding='utf-8') as f:
	json.dump(data, f, indent=4, ensure_ascii=False)