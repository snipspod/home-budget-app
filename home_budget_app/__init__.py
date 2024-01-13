import os
from flask import Flask
from dotenv import dotenv_values
from flask_wtf.csrf import CSRFProtect

secrets = dotenv_values('.env')


def create_app():

    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config.from_mapping(
        SECRET_KEY = secrets['SECRET_KEY'],
        MONGO_URI = secrets['MONGO_URI']
    )

    
    from . import auth
    from . import dashboard

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    
    app.add_url_rule('/', endpoint='dashboard.index')

    @app.template_filter()
    def format_datetime(value):
        from datetime import datetime
        date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        return date


    return app