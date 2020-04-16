from webapp import create_app
from webapp.ads.parsers import avito

app = create_app()
with app.app_context():
    # avito.get_ads_snippets()
    avito.get_ads_content()
