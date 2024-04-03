from flask import Flask
from datetime import timedelta
from dotenv import dotenv_values
from flask_wtf.csrf import CSRFProtect
from pymongo.mongo_client import MongoClient
import locale

secrets = dotenv_values('.env')


def create_app():

    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config.from_mapping(
        SECRET_KEY = secrets['SECRET_KEY'],
        MONGO_URI = secrets['MONGO_URI'],
        PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(secrets['SESSION_TIMEOUT']))
    )
    with app.app_context():
        try:
            app.db_connection = MongoClient(app.config['MONGO_URI'])
            print('connected to db!')
        except Exception as e:
            print(f'An exception occured while connecting to DB :: {e}')
            return e

    from . import auth
    from . import dashboard
    from . import expenses
    from . import user_account
    from . import categories
    from . import accounts
    from . import budgets

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(expenses.bp)
    app.register_blueprint(user_account.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(accounts.bp)
    app.register_blueprint(budgets.bp)
    
    app.add_url_rule('/', endpoint='dashboard.index')

    
    # DATE FILTER
    @app.template_filter()
    def format_date_from_string(value):
        from datetime import datetime
        date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        return date
    
    @app.template_filter()
    def format_datetime(value):
        lookup_table = {
            'styczeĹ„': 'stycznia',
            'luty': 'lutego',
            'marzec': 'marca',
            'kwiecieĹ„': 'kwietnia',
            'maj': 'maja',
            'czerwiec': 'czerwca',
            'lipiec': 'lipca',
            'sierpieĹ„': 'sierpnia',
            'wrzesieĹ„': 'września',
            'paĹşdziernik': 'października',
            'listopad': 'listopada',
            'grudzieĹ„': 'grudnia'
        }

        locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
        date = value.strftime("%d %B %Y")

        for key in lookup_table:
            date = date.replace(key, lookup_table[key])

        return date
    
    @app.template_filter()
    def format_date_to_monthyear(value):
        from datetime import datetime
        lookup_table = {
            'styczeĹ„': 'Styczeń',
            'luty': 'Luty',
            'marzec': 'Marzec',
            'kwiecieĹ„': 'Kwiecień',
            'maj': 'Maj',
            'czerwiec': 'Czerwiec',
            'lipiec': 'Lipiec',
            'sierpieĹ„': 'Sierpień',
            'wrzesieĹ„': 'Wrzesień',
            'paĹşdziernik': 'Październik',
            'listopad': ':Listopad',
            'grudzieĹ„': 'Grudzień'
        }

        locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
        date = datetime.strptime(value, "%Y-%m").strftime("%B %Y")

        for key in lookup_table:
            date = date.replace(key, lookup_table[key])

        return date
    
    return app