import json
import re

def clean_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Удалить все специальные символы из строк
    def clean_strings(obj):
        if isinstance(obj, dict):
            return {k: clean_strings(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_strings(v) for v in obj]
        elif isinstance(obj, str):
            # Удаление всех специальных символов
            return re.sub('[°®³±©™²’–—⁰“\u2011\u0099\u201d\u00a0\u00ba\u016b\u00e9\u03a9\u00b5\r\n\t]', '', obj)
            #re.sub(r'[\r\n\t]', '', obj)
            #obj.replace(', ' ').replase('\u00a0', ' ')
        else:
            return obj

    cleaned_data = clean_strings(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=True, indent=4)


# Указать пути к файлам
input_file_path = 'finish.json'
output_file_path = 'clean_all_data.json'

# Вызвать функцию для очистки файла
clean_json_file(input_file_path, output_file_path)
