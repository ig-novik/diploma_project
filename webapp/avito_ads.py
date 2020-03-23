import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from webapp.model import db, Ads, Img


DATE_FORMAT = '%d.%m.%Y %H:%M'
today = datetime.now()
yesterday = today - timedelta(days=1)


def str_to_date(str_):
    m = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }
    res = str_.replace('\n ', '')
    res = res.replace('\n', '')
    if res.find('Сегодня') != -1:
        res = res.replace('Сегодня', today.date().strftime('%d.%m.%Y'))
    elif res.find('Вчера') != -1:
        res = res.replace('Вчера', yesterday.date().strftime('%d.%m.%Y'))
    else:
        month_ = res.split()[1]
        if month_ in m:
            res = res.replace(' ' + month_ + ' ', '.' + m[month_] + '.' + str(today.year) + ' ')
        else:
            res = str_
    return res


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def save_ads(title, url, published):
    data_exists = Ads.query.filter(Ads.url == url).count()

    if not data_exists:
        new_ads = Ads(title=title, url=url, published=published)
        db.session.add(new_ads)
        db.session.commit()
        print(f'ad_id = {new_ads.id}')
        return new_ads.id
    else:
        return False


def save_images(alt, src, ad_id, published):
    data_exists = Img.query.filter(Img.src == src).count()

    if not data_exists:
        new_images = Img(alt=alt, src=src, ad_id=ad_id)
        db.session.add(new_images)
        db.session.commit()
        return new_images.id
    else:
        return False


def get_avito_ads():
    url_base = "https://www.avito.ru/rossiya/drugie_zhivotnye/reptilii-ASgBAgICAUSyA9AV?cd=1"
    html = get_html(url_base)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # определим количество вложенных страниц (пагинация)
        pgn = soup.find("div", attrs={"data-marker": "pagination-button"}).select('span')
        str_num = int(pgn[len(pgn) - 2].text)
        # парсим поочерёдно все страницы пагинации
        for num in range(str_num):
            html = get_html(url_base + '&p=' + str(num+1))
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                all_ads = soup.select('.item')
                for ad in all_ads:
                    title_row = ad.find('h3', class_='snippet-title')
                    title = title_row.text
                    url = 'https://www.avito.ru' + title_row.find('a')['href']
                    published = ad.find('div', class_='snippet-date-info').text.strip()
                    published = datetime.strptime(str_to_date(published), DATE_FORMAT)
                    ad_id = save_ads(title, url, published)
                    img_row = ad.select('img')
                    for img_ in img_row:
                        img_src = img_['src']
                        img_alt = img_['alt']
                        print(f' ads_id = {ad_id}')
                        img_id = save_images(img_alt, img_src, ad_id, published)
    else:
        print('Avito - не грузится')
