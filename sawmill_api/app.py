from flask import Flask

from sawmill_api.handlers.planks import planks_api


def make_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(planks_api)
    return app


if __name__ == "__main__":
    app = make_app()
    app.run(host="0.0.0.0")
