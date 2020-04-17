# import platform

from bs4 import BeautifulSoup

from webapp.db import db
from webapp.ads.models import Ads  # , Img

from webapp.ads.parsers.utils import get_html, save_ads, save_images
from webapp.ads.parsers.date import date_parse


def get_ads_snippets():
    url_base = "https://www.avito.ru/rossiya/drugie_zhivotnye/reptilii-ASgBAgICAUSyA9AV?cd=1&s=104"
    html = get_html(url_base)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # определим количество вложенных страниц (пагинация)
        pgn = soup.find("div", attrs={"data-marker": "pagination-button"}).select('span')
        str_num = int(pgn[len(pgn) - 2].text)
        # парсим поочерёдно все страницы пагинации
        for num in range(str_num):
            html = get_html(url_base + '&p=' + str(num + 1))
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                all_ads = soup.select('.item')
                for ad in all_ads:
                    title_row = ad.find('h3', class_='snippet-title')
                    title = title_row.text
                    url = 'https://www.avito.ru' + title_row.find('a')['href']
                    price = ad.find('span', class_='snippet-price').text.strip()
                    print(f' {title}, price = {price}')
                    if price == 'Бесплатно' or price == 'Цена не указана':
                        price = 0
                    else:
                        price = int(price[:-3].replace(' ', ''))
                    address = ad.find('span', class_='item-address__string').text
                    published = ad.find('div', class_='snippet-date-info')['data-tooltip']
                    print(published)
                    published = date_parse(published)
                    ad_id = save_ads(title, url, price, address, published)
                    img_row = ad.select('img')
                    for img_ in img_row:
                        img_src = img_['src']
                        img_alt = img_['alt']
                        print(f' ads_id = {ad_id}')
                        img_id = save_images(img_alt, img_src, ad_id)
    else:
        print('Avito - не грузится')


def get_ads_content():
    print("Вход в get_ads_content()")
    cnt = 1
    cnt_0 = 1
    ads_without_text = Ads.query.filter(Ads.text.is_(None)).all()
    for ad in ads_without_text:
        html = get_html(ad.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            article = soup.find('div', class_='item-view-content')
            if article:
                print(f'id = {ad.id}, url = {ad.url}')
                ads_text = article.decode_contents()
                if ads_text:
                    ad.text = ads_text
                    db.session.add(ad)
                    db.session.commit()
                if cnt > 15:
                    return True
                else:
                    cnt += 1
            else:
                print(f'Пустой контент, id = {ad.id}, url = {ad.url}')
                print(article)
                if cnt_0 > 9:
                    return False
                else:
                    cnt_0 += 1
        else:
            print(f'не прошёл: id = {ad.id}, url = {ad.url}')
