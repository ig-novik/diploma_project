from flask import current_app
import requests


def weather_by_city(city_name):
    weather_url = current_app.config["WEATHER_URL"]
    params = {
        "key": current_app.config["WEATHER_API_KEY"],
        "q": city_name,
        "num_of_days": 1,
        "format": "json",
        "lang": "ru"
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather_ = result.json()
        if 'data' in weather_:
            if 'current_condition' in weather_['data']:
                try:
                    return weather_['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
    return False


if __name__ == '__main__':
    w = weather_by_city("Moscow, Russia")
    print(w)
