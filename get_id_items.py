import json

def add_id_cards(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Начать нумерацию с 1
    id_counter = 1

    # Добавить id_card к каждому объекту в JSON
    for item in data:
        item['id_card'] = id_counter
        id_counter += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)

# Указать пути к файлам
input_file_path = 'test.json'
output_file_path = 'finish.json'

# Вызвать функцию для добавления id_card
add_id_cards(input_file_path, output_file_path)
