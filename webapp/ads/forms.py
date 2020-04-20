from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from webapp.ads.models import Ads


class CommentForm(FlaskForm):
    ads_id = HiddenField('ID объявления', validators=[DataRequired()])
    comment_text = StringField('Текст комментария', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    def validate_news_id(self, ads_id):
        if not Ads.query.get(ads_id.data):
            raise ValidationError('Вы пытаетесь прокомментировать объявление с несуществующим id')
