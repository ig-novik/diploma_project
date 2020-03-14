from flask import Flask, render_template

from webapp.model import db, Ads
from webapp.weather import weather_by_city


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route('/')
    def index():
        page_title = "Продажа пресмыкающихся"
        weather_ = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        ads_list = Ads.query.order_by(Ads.published.desc()).all()
        return render_template('index.html', page_title=page_title, weather=weather_, news_list=ads_list)

    return app
