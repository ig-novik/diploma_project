from flask import Flask, current_app
from flask_login import LoginManager

from webapp.user.forms import LoginForm
from webapp.db import db
from webapp.ads.models import Ads, Img
from webapp.admin.views import blueprint as admin_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.ads.views import blueprint as ads_blueprint
from webapp.weather import weather_by_city
from webapp.config import SQLALCHEMY_DATABASE_URI, POSTS_PER_PAGE
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(ads_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.context_processor
    def my_weather_context_processor():
        return dict(weather=weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"]))

    return app
