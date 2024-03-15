import json


def find_id_by_name(name, second_data):
    for item in second_data:
        if item['name'] == name:
            return item['id']
    return None


with open('clean_all_data.json', 'r', encoding='utf-8') as f1, open('list.json', 'r',
                                                                   encoding='utf-8') as f2:
    first_data = json.load(f1)
    second_data = json.load(f2)

for item in first_data:
    name = item['rubicator'].split(' | ')[-1]
    id_rub = find_id_by_name(name, second_data)
    if id_rub is not None:
        item['id_rub'] = id_rub

with open('correct.json', 'w') as f1:
    json.dump(first_data, f1, indent=4)
