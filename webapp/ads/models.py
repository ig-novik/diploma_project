from sqlalchemy.orm import relationship

from webapp.db import db

from datetime import datetime


class Ads(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Integer, default=0)
    address = db.Column(db.String)
    published = db.Column(db.DateTime, nullable=False, default=datetime.now())
    text = db.Column(db.Text)
    images = db.relationship("Img", backref="img_src")

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

    def comments_count(self):
        return Comment.query.filter(Comment.ads_id == self.id).count()

    def __repr__(self):
        return 'Ads {} {}>'.format(self.title, self.url)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    alt = db.Column(db.String, nullable=False)
    src = db.Column(db.String, unique=False, nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id', ondelete='SET NULL'))

    def __repr__(self):
        return 'Image {} {}>'.format(self.alt, self.src)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    ads_id = db.Column(
        db.Integer,
        db.ForeignKey('ads.id', ondelete='CASCADE'),
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )
    ads = relationship('Ads', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.id)
