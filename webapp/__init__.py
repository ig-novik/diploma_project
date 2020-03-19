from flask import Flask, render_template

from webapp.forms import LoginForm
from webapp.model import db, Ads, Img
from webapp.weather import weather_by_city
from webapp.config import SQLALCHEMY_DATABASE_URI


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route('/')
    def index():
        page_title = "Продажа пресмыкающихся"
        weather_ = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        ads_list = Ads.query.order_by(Ads.published.desc()).all()

        return render_template('index.html', page_title=page_title, weather=weather_, ads_list=ads_list)

    @app.route('/login')
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    return app
