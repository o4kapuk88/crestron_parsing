import time
from playwright.sync_api import sync_playwright


def parse_items_link():
    with open('links_inner.txt', 'r') as f:
        urls = f.readlines()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, timeout=60000)
        content = browser.new_context()
        page = content.new_page()

        # Ваш код начинается здесь
        for url in urls:
            url = url.strip()
            page.goto(url)
            time.sleep(10)
            # Вызываем функцию, которая кликает на кнопку и дожидается загрузки
            load_more_until_done(page)
            time.sleep(3)
            # Теперь, когда все элементы загружены, ищем ссылки
            divs = page.query_selector_all('div.model-number-wrapper')
            for div in divs:
                link = div.query_selector('a')
                href = link.get_attribute('href')

                with open('links_items.txt', 'a', encoding='utf-8') as f:
                    f.write(href + '\n')

        browser.close()


def load_more_until_done(page):
    btn_more = page.query_selector('span#btnMore')

    while btn_more and btn_more.is_visible():
        btn_more.click()
        time.sleep(1)
        page.wait_for_load_state('networkidle')
        btn_more = page.query_selector('span#btnMore')


parse_items_link()
