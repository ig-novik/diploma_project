import os

basedir = os.path.abspath(os.path.dirname(__file__))

print(os.path.join(basedir, '..', 'webapp.db'))

WEATHER_DEFAULT_CITY = "Moscow,Russia"
WEATHER_API_KEY = "ad4d399064a146bd8f4140022200303"
WEATHER_URL = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')