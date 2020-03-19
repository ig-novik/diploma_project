from flask_sqlalchemy import SQLAlchemy

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



    @property
    def all_ad_images_src(self):
        print(f'номер объявления  {self.img_ad_id}')
        if self.id == self.img_ad_id:
            if self.images:
                return [img.src for img in self.images]
            return []
        return []

    @all_ad_images_src.setter
    def all_ad_images_src(self, value):
        self.img_ad_id = value

    def __repr__(self):
        return 'Ads {} {}>'.format(self.title, self.url)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    alt = db.Column(db.String, nullable=False)
    src = db.Column(db.String, unique=False, nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id', ondelete='SET NULL'))

    def __repr__(self):
        return 'Image {} {}>'.format(self.alt, self.src)
