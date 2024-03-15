import json

# Открываем файл с товарами
with open('clean_all_data.json', 'r', encoding='utf-8') as f:
    all_products = json.load(f)

# Создаем словарь, который будет использоваться для хранения иерархии категорий
category_dict = {}


# Функция для создания категории и уникального id
def create_category(category_name, parent_id):
    category_id = len(category_dict) + 1
    category_dict[category_name] = {'id': category_id, 'parent_id': parent_id, 'name': category_name}
    return category_id


# Проходим по каждому товару и создаем словарь для категории товара
for product in all_products:
    breadcrumb_contain = product['rubicator']
    categories = breadcrumb_contain.split(' | ')[1:]

    # Создаем словарь для верхнего уровня, если он еще не создан
    if categories[0] not in category_dict:
        create_category(categories[0], 0)

    # Создаем словари для остальных уровней, начиная с id = 2
    parent_id = category_dict[categories[0]]['id']
    for i in range(1, len(categories)):
        # Создаем категорию, если она еще не создана
        if categories[i] not in category_dict:
            parent_id = create_category(categories[i], parent_id)
        else:
            # Если категория уже существует, то используем ее id
            parent_id = category_dict[categories[i]]['id']

# Сохраняем словарь в файл 'breadcrumb_contain_dict.json'
with open('list.json', 'w', encoding='utf-8') as f:
    json.dump(list(category_dict.values()), f, ensure_ascii=False, indent=4)
