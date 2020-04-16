from datetime import datetime, timedelta

DATE_FORMAT = '%d.%m.%Y %H:%M'
today = datetime.now()
yesterday = today - timedelta(days=1)


def date_parse(str_):
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
    if res:
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
        return datetime.strptime(res, DATE_FORMAT)
    else:
        return datetime.now() - timedelta(days=31)
