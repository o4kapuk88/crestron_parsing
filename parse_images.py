import aiohttp
import os
import json
import asyncio
from aiofiles import open as aio_open
from bs4 import BeautifulSoup

response = aiohttp.ClientSession()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}

# Отключение проверки SSL
response.connector._ssl = False

# Ограничиваем количество одновременных запросов
semaphore = asyncio.Semaphore(1)  # Ограничивает количество одновременных запросов до 10


async def fetch_images(item):
    async with semaphore:
        id_card = str(item['id_card'])  # Преобразование int в str
        url = item['url']
        async with response.get(url=url, headers=headers) as resp:
            soup = BeautifulSoup(await resp.text(), 'lxml')
            try:
                # Извлекаем все теги a внутри div с классом mz-item и hide-for-small-only
                images = soup.find_all('div', class_='model-alt-images')
                # Проверяем, есть ли на странице теги с классом gallery-button
                if images:
                    for index, correct_url in enumerate(images, start=1):  # Задаем индекс от 1
                        # Получаем все теги a внутри текущего div
                        links = correct_url.find_all('a')
                        for link in links:
                            # Получаем href для каждого тега a
                            data_large = link['href']
                            if data_large:
                                # Получение пути к изображению
                                image_url = data_large
                                print(image_url)
                                # Получаем путь к папке с id_card
                                folder_path = os.path.join('images', id_card)
                                # Создаем папку, если ее нет
                                os.makedirs(folder_path, exist_ok=True)
                                # Сохраняем изображение в папку
                                image_filename = f'{id_card}_{index}.jpg'
                                image_path = os.path.join(folder_path, image_filename)

                                # Сохранение изображения
                                async with response.get(image_url, timeout=10) as response_image:
                                    if response_image.status == 200:
                                        async with aio_open(image_path, 'wb') as image_file:
                                            image_data = await response_image.read()
                                            await image_file.write(image_data)
                                    else:
                                        # Если статус ответа не 200, записываем данные в fail_urls.txt
                                        async with aio_open('fail_urls.txt', 'a') as fail_urls:
                                            await fail_urls.write(f'ID: {id_card}, URL: {url}\n')
                            else:
                                print("Атрибут 'data-large' отсутствует")
                                async with aio_open('fail_url.txt', 'a') as fail_urls:
                                    await fail_urls.write(f'ID: {id_card}, URL: {url}\n')
            except aiohttp.client_exceptions.ServerDisconnectedError as e:
                print(f"Ошибка при обработке URL: {url}, {e}")
            except Exception as e:
                async with aio_open('error_log.txt', 'a') as error_log:
                    await error_log.write(f'URL: {url}, ID: {id_card}\n')
                print(f"Ошибка при обработке URL: {url}")
        print(f"Страница обработана: {url}")


async def main():
    # Получение списка папок в директории images
    folder_list = [f for f in os.listdir('images') if os.path.isdir(os.path.join('images', f))]
    # Получение списка номеров id_card из папок в директории images
    id_card_numbers = [int(folder_name.split('_')[0]) for folder_name in folder_list]

    # Считывание данных из файла finish.json
    with open('correct.json', 'r', encoding='utf-8') as file_urls:
        datas = json.load(file_urls)

        # # Получение последнего номера id_card из папок в директории images
        # last_id_card = max(id_card_numbers) if id_card_numbers else 0
        #
        # # Получение данных из файла finish.json, начиная с последнего id_card
        # datas = [data for data in datas if data['id_card'] >= last_id_card]
        #
        # await asyncio.gather(*[fetch_images(item) for item in datas])

    # Получение списка id_card из файла id_card, которых нет в папке images
    with open('missing_numbers.txt', 'r', encoding='utf-8') as file_id_card:
        missing_id_card = [int(line.strip()) for line in file_id_card if int(line.strip()) not in id_card_numbers]

        # Получение данных из файла finish.json, начиная с последнего id_card
        datas = [data for data in datas if data['id_card'] in missing_id_card]

        await asyncio.gather(*[fetch_images(item) for item in datas])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
