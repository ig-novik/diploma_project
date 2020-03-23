from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Ads(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    images = db.relationship("Img", backref="img_src")
    img_ad_id = None

    @property
    def first_image_src(self):
        if self.images:
            return self.images[0].src
        return ""

    @property
    def all_ads_images_src(self):
        if self.images:
            return [img.src for img in self.images]
        return []

    @staticmethod
    def img_src_for_ad_id(id_):

        res = []
        for ad in Ads.query.all():
            for im in ad.images:
                if im.ad_id == id_:
                    res.append(im.src)
        return res

    def __repr__(self):
        return 'Ads {} {}>'.format(self.title, self.url)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    alt = db.Column(db.String, nullable=False)
    src = db.Column(db.String, unique=False, nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id', ondelete='SET NULL'))

    def __repr__(self):
        return 'Image {} {}>'.format(self.alt, self.src)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User name = {}, id = {}>'.format(self.username, self.id)
