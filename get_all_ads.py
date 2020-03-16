from webapp import create_app
from webapp.avito_ads import get_avito_ads

app = create_app()
with app.app_context():
    get_avito_ads()
