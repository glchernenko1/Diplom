from src.config import app_config

from src.view import api as api_blueprint

from flask import Flask, Response, json

import os


def create_app(env_name):
    app = Flask(
        __name__,
        static_url_path='',
        static_folder='frontend/dist')

    app.config.from_object(app_config[env_name])

    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/', methods=['GET'])
    def index():
        return app.send_static_file('index.html')

    return app
