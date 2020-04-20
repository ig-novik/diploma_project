from flask import abort, Blueprint, flash, current_app, render_template, redirect, request
from flask_login import current_user, login_required

from webapp.db import db
from webapp.ads.forms import CommentForm
from webapp.ads.models import Comment, Ads
from webapp.utils import get_redirect_target

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
    ads_list = Ads.query.filter(Ads.text.isnot(None)).order_by(Ads.published.desc()).paginate(page, current_app.config[
        "POSTS_PER_PAGE"], False)

    return render_template('ads/index.html', page_title=page_title, ads_list=ads_list)


@blueprint.route('/ads/<int:ads_id>')
def single_ad(ads_id):
    my_ad = Ads.query.filter(Ads.id == ads_id).first()

    if not my_ad:
        abort(404)
    comment_form = CommentForm(ad_id=my_ad.id)
    return render_template('ads/single_ad.html', ad=my_ad,  comment_form=comment_form)


@blueprint.route('/ads/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment_text.data, ads_id=form.ad_id.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий успешно добавлен')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в заполнении поля "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target())
