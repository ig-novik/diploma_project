from webapp import db, create_app
from sqlalchemy import create_engine
from webapp.config import SQLALCHEMY_DATABASE_URI

db.create_all(app=create_app())

#создаём представление (вьюху) с нужным набором данных
e = create_engine(SQLALCHEMY_DATABASE_URI)
e.execute('''CREATE VIEW ads_img AS
select ads.id as ad_id, ads.title as ad_title, ads.url as ad_url, (select img.src from img where img.ad_id = ads.id limit 1) as img_src, ads.published as ad_date from ads''')
