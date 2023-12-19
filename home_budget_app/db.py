from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app


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
    users_collection = client.mongo_client["User"]["Users"]

    initial_profile = {
        'net_value': 0
    }

    user = {
        'email': email,
        'password': password_hash,
        'name': name,
        'profile': initial_profile
    }

    users_collection.insert_one(user)