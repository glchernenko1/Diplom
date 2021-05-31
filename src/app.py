from src.config import app_config

from src.view import api as api_blueprint

from flask import Flask, Response, json


def create_app(env_name):
    app = Flask(__name__, root_path='')
    app.config.from_object(app_config[env_name])

    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/', methods=['GET'])
    def index():
        return Response(json.dumps({
            "success": True,
            "data": "Index page"
        }), status=200, content_type='application/json')

    return app
