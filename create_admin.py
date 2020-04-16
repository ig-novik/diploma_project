from getpass import getpass
import sys

from webapp import create_app
from webapp.user.models import db, User

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')
    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)
    email = input('Введите e-mail: ')
    if User.query.filter(User.email == email).count():
        print('Такой e-mail уже есть')
        sys.exit(0)
    password1 = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password1 == password2:
        print('Ведённые пароли не совпадают')
        sys.exit(0)
    new_user = User(username=username, role='admin', email=email)
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))
