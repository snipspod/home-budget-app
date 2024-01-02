from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
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

    user = {
        'email': email,
        'password': password_hash,
        'name': name,
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
        'status': 'active'
    }

    try:
        users_collection.insert_one(user)
    except Exception as e:
        return e
    
    client.close()

def get_user(email, password):
    client = connect_db()
    users_collection = client.mongo_client["User"]["Users"]

    user = users_collection.find_one({'email': email})

    if user is not None:
        if check_password_hash(user.get('password'), password):
            return True
        else:
            raise ValueError(f"Wrong password!")
    else:
        raise ValueError(f"User {email} does not exists!")
    
    client.close()
    
