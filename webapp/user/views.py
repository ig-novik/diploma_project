from flask import render_template, flash, redirect, url_for, Blueprint, current_app
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm
from webapp.user.models import User
from webapp.weather import weather_by_city

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ads.index'))
    title = "Авторизация"
    login_form = LoginForm()
    weather_ = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    return render_template('user/login.html', page_title=title, form=login_form,  weather=weather_)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('ads.index'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('ads.index'))
