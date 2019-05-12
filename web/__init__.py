from flask import Flask, Blueprint

from instance.config import config
from .api.routes import fr
from .api.models import db
from .api.data import create_clients_and_products


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    app.register_blueprint(fr)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_clients_and_products(db)

    return app
