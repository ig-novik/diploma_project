from flask import abort, Blueprint, current_app, request, render_template

from webapp.ads.models import Ads

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
    ads_list = Ads.query.filter(Ads.text.isnot(None)).order_by(Ads.published.desc()).paginate(page, current_app.config["POSTS_PER_PAGE"], False)

    return render_template('ads/index.html', page_title=page_title, ads_list=ads_list)


@blueprint.route('/ads/<int:ads_id>')
def single_ad(ads_id):
    my_ad = Ads.query.filter(Ads.id == ads_id).first()

    if not my_ad:
        abort(404)

    return render_template('ads/single_ad.html', page_title=my_ad.title, text=my_ad.text)
