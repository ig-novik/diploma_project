from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from webapp.ads.models import Ads


class CommentForm(FlaskForm):
    ad_id = HiddenField('ID объявления', validators=[DataRequired()])
    comment_text = StringField('Текст комментария', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    def validate_ad_id(self, ad_id):
        if not Ads.query.get(ad_id.data):
            raise ValidationError('Вы пытаетесь прокомментировать объявление с несуществующим id')
