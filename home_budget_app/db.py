from pymongo import ASCENDING, DESCENDING
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from home_budget_app.utils import parse_json
from bson import ObjectId


def create_user(name, email, password):
    DB = app.db_connection.home_budget_app
    password_hash = generate_password_hash(password)
    users_collection = DB["Users"]

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
        'budgets': []
    }

    if users_collection.find_one({'email': email}) is None:
        try:
            users_collection.insert_one(user)
        except Exception as e:
            return e
    else:
        raise ValueError(f"User {email} already exists!")
    
 
def add_single_expense(email, amount, date, account, category, description):
    DB = app.db_connection.home_budget_app
    expenses_collection = DB["Expenses"]

    expense = {
        'email': email,
        'description': description,
        'category': category,
        'account': account,
        'amount': amount,
        'date_at': date,
        'date_submitted': datetime.datetime.now(),
        'type': 'none'
    }
    
    try:
        expenses_collection.insert_one(expense)
        return {'result': 'success',
                'message': 'Pomyślnie dodano wydatek!'}
    except Exception as e:
        return {'result': 'danger',
                'message': e}


#! UPDATE METHODS
        

def update_password(email, old_password, new_password):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]

        current_password = users_collection.find_one({'email': email}, projection={'password':True})['password']

        if check_password_hash(current_password, old_password):
            users_collection.find_one_and_update({'email': email}, {'$set': {'password': generate_password_hash(new_password)}})
            return {'result': 'success',
                    'message': 'Pomyślnie zmieniono hasło!'}
        else:
            return {'result': 'danger',
                    'message': 'Podane obecne hasło nie jest poprawne!'}
        
    except Exception as e:
        return {'result': 'danger',
                'message': e}
    

def update_expense(expense_id, amount, category, date, account, description):
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB["Expenses"]

        expense_id = ObjectId(expense_id)

        expenses_collection.find_one_and_update({'_id': expense_id}, {'$set': {'amount': amount, 'category': category, 'date': date, 'account': account, 'description': description}})

        return {'result': 'success',
                'message': 'Pomyślnie zaktualizowano wydatek!'}
    except Exception as e:
        return {'result': 'danger',
                'message': e} 




#! GET METHODS


def authenticate_user(email, password):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]

        user = users_collection.find_one({'email': email})

        if user is not None:
            if check_password_hash(user.get('password'), password) and user.get('status') == 'active':
                return parse_json(user)
            elif user.get('status') != 'active':
                raise ValueError(f'User is not active!')
            else:
                raise ValueError(f"Wrong password!")
        else:
            raise ValueError(f"User {email} does not exists!")
    except Exception as e:
        return e


def get_user_by_email(email):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]
        user = users_collection.find_one({'email': email}, projection={'password':False})
        return parse_json(user)
    except Exception as e:
        return e
    

def get_user_categories(email):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]
        categories = users_collection.find_one({'email': email}, projection={'categories':True})['categories']
        return parse_json(categories)
    except Exception as e:
        return e
    
def get_user_accounts(email):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]
        accounts = users_collection.find_one({'email': email}, projection={'accounts':True})['accounts']
        return parse_json(accounts)
    except Exception as e:
        return e
    
def get_user_expenses(email, limit:int=0):
    """Returns user expenses. Amount of returned documents can be limited by specifying second **parameter**."""

    
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB["Expenses"]
        
        expenses = expenses_collection.find({'email': email},limit=limit, sort=[('date_at', DESCENDING)])

        return parse_json(expenses)
    except Exception as e:
        return e
    
def get_user_statistics(email):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]
        expenses_collection = DB["Expenses"]

        member_from = users_collection.find_one({'email': email}, projection={'created_at': True})['created_at']

        expense_count = expenses_collection.count_documents({'email': email})

        expense_sum = expenses_collection.aggregate([{'$match': {'email': email}}, {'$group': {'_id': None, 'sum': {'$sum': '$amount'}}}])
        expense_sum = parse_json(expense_sum)[0]['sum']

        account_sum = users_collection.find({'email': email}, {'sum': {'$sum': '$accounts.current_balance'}})
        account_sum = parse_json(account_sum)[0]['sum']

        #TODO: kalkulowanie sredniej wydatków za ostatnie 30 dni

        return {
            'member_from': member_from,
            'expense_count': expense_count,
            'expense_sum': round(expense_sum, 2),
            'accounts_sum': account_sum,
            'expense_avg': 2137
        }


    except Exception as e:
        return e
