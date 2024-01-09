from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from bson import json_util
import json


def connect_db():
    client = MongoClient(app.config['MONGO_URI'], server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print('succesfully connected to mongoDB!')
    except Exception as e:
        print(e)

    return client

def create_user(name, email, password):
    client = connect_db()
    password_hash = generate_password_hash(password)
    users_collection = client.home_budget_app["Users"]

    user = {
        'email': email,
        'password': password_hash,
        'name': name,
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
        'status': 'active',
        'categories': [
            'Spożywcze', 'Dom', 'Jedzenie poza domem', 'Kosmetyki', 'Podróże', 'Rozrywka', 'Edukacja'
            ],
        'accounts': [],
        'budgets': [],
        'expenses': [],
    }

    if users_collection.find_one({'email': email}) is None:
        try:
            users_collection.insert_one(user)
            client.close()
        except Exception as e:
            return e
    else:
        raise ValueError(f"User {email} already exists!")
    
 
def add_single_expense(email, amount, transactionType, date, account, category, description):
    client = connect_db()
    users_collection = client.home_budget_app["Users"]

    expense = {
        'description': description,
        'category': category,
        'account': account,
        'amount': amount,
        'date_at': date,
        'date_submitted': datetime.datetime.now(),
        'type': transactionType
    }
    
    try:
        users_collection.find_one_and_update({'email': email}, {'$push':{'expenses': expense}})
    except Exception as e:
        print(e)


# GET METHODS


def get_user(email, password):
    client = connect_db()
    users_collection = client.home_budget_app["Users"]

    user = users_collection.find_one({'email': email})
    client.close()

    if user is not None:
        if check_password_hash(user.get('password'), password) and user.get('status') == 'active':
            return parse_json(user)
        elif user.get('status') != 'active':
            raise ValueError(f'User is not active!')
        else:
            raise ValueError(f"Wrong password!")
    else:
        raise ValueError(f"User {email} does not exists!")
        

def get_user_by_email(email):
    try:
        client = connect_db()
        users_collection = client.home_budget_app["Users"]
        user = users_collection.find_one({'email': email}, projection={'password':False})
        client.close()
        return parse_json(user)
    except Exception as e:
        return e
    

def get_user_categories(email):
    try:
        client = connect_db()
        users_collection = client.home_budget_app["Users"]
        categories = users_collection.find_one({'email': email}, projection={'categories':True})['categories']
        client.close()
        return parse_json(categories)
    except Exception as e:
        return e
    
def get_user_accounts(email):
    try:
        client = connect_db()
        users_collection = client.home_budget_app["Users"]
        accounts = users_collection.find_one({'email': email}, projection={'accounts':True})['accounts']
        client.close()
        return parse_json(accounts)
    except Exception as e:
        return e

# UTILITY METHODS

    
def parse_json(data):
    return json.loads(json_util.dumps(data))
    
