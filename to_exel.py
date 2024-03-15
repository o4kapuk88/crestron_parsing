import pandas as pd

# Прочитайте JSON-файл в DataFrame
df = pd.read_json('finish.json')

# Выберите столбцы 'title' и 'name'
df = df[['title', 'breadcrumb_contain']]

# Запишите DataFrame в файл Excel
df.to_excel('commscope_exel.xlsx', index=False)
