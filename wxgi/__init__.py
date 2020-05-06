from flask import Flask
from wxgi import settings
from wxgi import views


def create_app():
    app = Flask(__name__)

    app.config.from_object(settings)

    app.register_blueprint(views.bp)

    return app