import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from webapp.db import db, Ads, Img


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


html = get_html("https://www.avito.ru/rossiya/drugie_zhivotnye/reptilii-ASgBAgICAUSyA9AV?cd=1")
if html:
    soup = BeautifulSoup(html, 'html.parser')
    strings = soup.find_all("span", class_="pagination-item-1WyVp")
    print(strings[len(strings) - 2].text)
    str2 = soup.find("div", attrs={"data-marker": "pagination-button"}).select('span')
    print(str2[len(str2) - 2].text)
    pgn = soup.find("div", attrs={"data-marker": "pagination-button"}).select('span')
    str_num = int(pgn[len(pgn) - 2].text)
    print(str(str_num))
for number in range(str_num):
    print(number)
