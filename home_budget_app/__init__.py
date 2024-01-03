import os
from flask import Flask
from dotenv import dotenv_values

secrets = dotenv_values('.env')

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = secrets['SECRET_KEY'],
        MONGO_URI = secrets['MONGO_URI']
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import auth
    from . import dashboard

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    
    app.add_url_rule('/', endpoint='dashboard.index')

    return app