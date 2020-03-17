from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ads(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    images = db.relationship("Img", backref="img_src")

    @property
    def first_image_src(self):
        if self.images:
            return self.images[0].src
        return ""

    def __repr__(self):
        return 'Ads {} {}>'.format(self.title, self.url)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    alt = db.Column(db.String, nullable=False)
    src = db.Column(db.String, unique=False, nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id', ondelete='SET NULL'))

    def __repr__(self):
        return 'Image {} {}>'.format(self.alt, self.src)
