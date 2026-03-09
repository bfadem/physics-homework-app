import os

from flask import Flask

from .models import db
from .routes import bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=db_url or "sqlite:///app.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        ADMIN_TOKEN=os.getenv("ADMIN_TOKEN", ""),
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(bp)

    return app
