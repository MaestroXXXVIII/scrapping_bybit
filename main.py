import csv
import time

from selenium import webdriver
from bs4 import BeautifulSoup


def scrape_bybit():

    found_news = set()

    # Количество страниц новостей, которые нужно парсить + 1
    pages = 2

    while True:
        for page in range(1, pages):
            try:
                url = f"https://announcements.bybit.com/ru-RU/" \
                      f"?category=&page={page}"
                driver = webdriver.Chrome()
                driver.get(url)

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                news = soup.find_all('a', class_="no-style")

                for n in news:
                    date = (n.find('div', class_='article-item-date')
                             .text.strip())
                    title = n.find('span').text.strip()
                    link = n['href']
                    link = f'https://www.bybit.com/{link}'

                    if link not in found_news:
                        found_news.add(link)

                        with open("bybit_news.csv", "a", newline="",
                                  encoding="utf-8") as file:
                            writer = csv.writer(file)
                            writer.writerow([date, title, link])
                            print("Новость сохранена:", date, title, link)

            except Exception as ex:
                print("Возникла ошибка:", str(ex))

            time.sleep(1)


scrape_bybit()
