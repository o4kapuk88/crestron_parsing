import asyncio
import json
import playwright.async_api
import random


async def main():
    # Открываем файл с сылками на товары
    with open('links_items.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()

    async with playwright.async_api.async_playwright() as p:
        # Запускаем браузер
        browser = await p.chromium.launch()
        # Создаём новую вкладку
        context = await browser.new_context()
        # Создаём пустой список для результатов
        results = []

        for url in urls:
            attempts = 3  # Ограничение на количество попыток загрузки страницы
            while attempts > 0:
                try:
                    # Переходим по ссылке на товар
                    page = await context.new_page()
                    await page.goto(url, timeout=60000)

                    await page.wait_for_selector('div#panel2')

                    # Получаем данные о товаре
                    data = await page.evaluate('''() => {
                        const rows = Array.from(document.querySelectorAll('div#panel2 table tbody tr'));
                        const title = document.querySelector('p.model-name').innerText.trim();
                        const rubicator = Array.from(document.querySelectorAll('div.column.medium-13.elips.align-middle > a'))
                                                .map(a => a.innerText.trim())
                                                .join(' | ');
                        const title_wrapper = document.querySelector('p.model-title').innerText.trim();
                        const description_wrapper = (document.querySelector('div.model-short-description > p') || document.querySelector('div.model-short-description')).innerText.trim();
                        const specification = rows.map(row => Array.from(row.querySelectorAll('td'))
                                                    .map(td => td.innerText.trim())
                                                    .join('')).join(' ');

                        return {
                            title,
                            rubicator,
                            title_wrapper,
                            description_wrapper,
                            specification,
                        };
                    }''')

                    # Добавляем результаты в список
                    results.append({
                        'url': url.strip(),
                        **data,
                    })

                    # Закрываем текущую вкладку
                    await page.close()
                    # Выходим из цикла, если загрузка прошла успешно
                    break
                except Exception as e:
                    print(f"Error loading URL: {url}, error: {e}")
                    attempts -= 1
                    if attempts == 0:
                        print(f"Skipping URL: {url}, max attempts exceeded")
                        # Закрываем текущую вкладку
                        await page.close()
                        break
                    else:
                        # Пауза перед следующей попыткой загрузки
                        await asyncio.sleep(random.uniform(1.0, 3.0))
                        continue

        # Закрываем браузер
        await browser.close()

    # Сохраняем результаты в файл
    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        f.write(',\n')  # Добавляется перенос строки
if __name__ == "__main__":
    asyncio.run(main())
