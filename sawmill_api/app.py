from flask import Flask

from sawmill_api.handlers.planks import planks_api
from sawmill_api.handlers.settings import settings_api
from sawmill_api import wsgi, settings
from sawmill_api.lib import oltp


def make_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(planks_api)
    app.register_blueprint(settings_api)
    db = oltp.BlockingConnectionPool(
        host=wsgi.OLTPDatabase.host,
        port=wsgi.OLTPDatabase.port,
        user=wsgi.OLTPDatabase.user,
        password=wsgi.OLTPDatabase.password,
        dbname=wsgi.OLTPDatabase.dbname,
        max_connections=wsgi.OLTPDatabase.max_connections,
    )
    db.init_app(app)
    app_settings = oltp.get_api_settings()
    settings.populate(grouped_by_section=app_settings)

    return app


if __name__ == "__main__":
    app = make_app()
    app.run(host="0.0.0.0")
