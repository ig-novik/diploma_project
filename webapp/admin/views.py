from flask import Blueprint, render_template, current_app
from webapp.user.decorators import admin_required
from webapp.weather import weather_by_city

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = "Панель управления"
    weather_ = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    return render_template('admin/index.html', page_title=title, weather=weather_)
