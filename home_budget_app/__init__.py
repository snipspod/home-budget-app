import os
from flask import Flask
from dotenv import dotenv_values
from flask_wtf.csrf import CSRFProtect
from pymongo.mongo_client import MongoClient

secrets = dotenv_values('.env')


def create_app():

    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config.from_mapping(
        SECRET_KEY = secrets['SECRET_KEY'],
        MONGO_URI = secrets['MONGO_URI']
    )
    with app.app_context():
        try:
            app.db_connection = MongoClient(app.config['MONGO_URI'])
            print('connected to db!')
        except Exception as e:
            print(e)
            return e

    from . import auth
    from . import dashboard
    from . import expenses
    from . import user_account

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(expenses.bp)
    app.register_blueprint(user_account.bp)
    
    app.add_url_rule('/', endpoint='dashboard.index')

    # DATE FILTER
    @app.template_filter()
    def format_datetime(value):
        from datetime import datetime
        date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        return date


    return app