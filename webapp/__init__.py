from flask import Flask, render_template

from webapp.model import db, Ads, Img
from webapp.weather import weather_by_city
from sqlalchemy import create_engine
from webapp.config import SQLALCHEMY_DATABASE_URI


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route('/')
    def index():
        page_title = "Продажа пресмыкающихся"
        weather_ = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        e = create_engine(SQLALCHEMY_DATABASE_URI)
        ads_list = []
        for u in e.execute('select * from one_img_per_ad'):
            ads_list.append(u)

        return render_template('index.html', page_title=page_title, weather=weather_, ads_list=ads_list)

    return app
