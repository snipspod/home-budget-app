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

    @app.route("/")
    def index(): 
        return "Budget App!"
    
    from . import auth

    app.register_blueprint(auth.bp)

    
    return app