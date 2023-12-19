import os
from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI='mongodb+srv://dbAdmin:E2W$WI7uN3C&5q6G@cluster0.2zz1f2k.mongodb.net/?retryWrites=true&w=majority'
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