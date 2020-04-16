import requests

from webapp.db import db
from webapp.ads.models import Ads, Img


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print(f"Сетевая ошибка, url = {url} ")
        return False


def save_ads(title, url, price, address, published):
    data_exists = Ads.query.filter(Ads.url == url).count()

    if not data_exists:
        new_ads = Ads(title=title, url=url, price=price, address=address, published=published)
        db.session.add(new_ads)
        db.session.commit()
        print(f'ad_id = {new_ads.id}')
        return new_ads.id
    else:
        return False


def save_images(alt, src, ad_id):
    data_exists = Img.query.filter(Img.src == src).count()

    if not data_exists:
        new_images = Img(alt=alt, src=src, ad_id=ad_id)
        db.session.add(new_images)
        db.session.commit()
        return new_images.id
    else:
        return False
