from flask import Blueprint, current_app, request, render_template

from webapp.ads.models import Ads
from webapp.weather import weather_by_city

blueprint = Blueprint('ads', __name__)


@blueprint.route('/', methods=['POST', 'GET'])
def index(page=1):
    pg = request.args.get('page', '')
    if pg:
        page = int(pg)
    else:
        page = 1
    print(f'page = {pg}')
    page_title = "Продажа рептилий и террариумов в России"
    weather_ = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    ads_list = Ads.query.order_by(Ads.published.desc()).paginate(page, current_app.config["POSTS_PER_PAGE"], False)

    return render_template('index.html', page_title=page_title, weather=weather_, ads_list=ads_list)
