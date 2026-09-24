import os
from flask import Flask
from .db import init_db

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-me-in-production")
    init_db()

    from .routes import bp
    app.register_blueprint(bp)
    return app
