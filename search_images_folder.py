import os

# Список всех папок в текущем каталоге
folders = os.listdir('images')

# Список всех возможных номеров от 1 до 55178
all_numbers = set(range(1, 1761))

# Список отсутствующих номеров
missing_numbers = all_numbers - set(map(int, folders))

# Сортировка номеров
missing_numbers = sorted(missing_numbers)

# Запись номеров в файл
with open('missing_numbers.txt', 'w') as file:
    for number in missing_numbers:
        file.write(str(number) + '\n')

print('Done! Missing numbers written to "missing_numbers.txt"')
