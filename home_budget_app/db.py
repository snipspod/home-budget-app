from pymongo import ASCENDING, DESCENDING
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'status': 'active',
        'categories': [
            'Spożywcze', 'Dom', 'Jedzenie poza domem', 'Kosmetyki', 'Podróże', 'Rozrywka', 'Edukacja'
            ]
    }

    if users_collection.find_one({'email': email}) is None:
        try:
            users_collection.insert_one(user)
            return {'result': 'success',
                    'message': {'header': 'Udało się!',
                                'message': 'Użytkownik pomyślnie zarejestrowany!'}}
        except Exception as e:
            return {'result': 'danger',
                    'message': {'header': 'Nieznany błąd',
                                'message': e}}
    else:
        return {'result': 'danger',
                'message': {'header': 'Niepowodzenie',
                            'body': 'Użytkownik z takim mailem już istnieje!'}}
    
 
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
        'date_submitted': datetime.now(),
    }
    
    try:
        expenses_collection.insert_one(expense)
        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie dodano wydatek!'}}
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd',
                            'body': e }}
    

def add_category(email, category):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB['Users']

        users_collection.update_one({'email': email}, {'$push': {'categories': category}})

        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie dodano kategorię!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 
    

def add_account(email, account_name, start_balance, cyclical,income_amount, income_day):
    try:
        DB = app.db_connection.home_budget_app
        accounts_collection = DB['Accounts']

        if accounts_collection.find_one({'email': email, 'name': account_name}):
            return {'result': 'danger',
                'message': {'header': 'Nie udało się.',
                            'body': 'Konto o podanej nazwie istnieje już na Twoim koncie. Spróbuj ponownie, używając innej nazwy.'}}
        
        next_income_date = datetime(datetime.now().year, datetime.now().month, int(income_day))

        if not next_income_date.day > datetime.now().day:
            next_income_date = next_income_date + relativedelta(months=1)

        account = {
            'email': email,
            'name': account_name,
            'balance': start_balance,
            'income_active': cyclical,
            'income': income_amount,
            'next_income_date': next_income_date
        }
        accounts_collection.insert_one(account)
        
        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie dodano konto!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 
    

#! UPDATE METHODS
        

def update_password(email, old_password, new_password):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]

        current_password = users_collection.find_one({'email': email}, projection={'password':True})['password']

        if check_password_hash(current_password, old_password):

            if old_password == new_password:
                return {'result': 'danger',
                        'message': {'header': 'Nie udało się!',
                                    'body': 'Stare i nowe hasło muszą się od siebie różnić!'}}
        
            users_collection.find_one_and_update({'email': email}, {'$set': {'password': generate_password_hash(new_password)}})
            return {'result': 'success',
                    'message': {'header': 'Udało się!',
                                'body': 'Pomyślnie zmieniono hasło!'}}
        else:
            return {'result': 'danger',
                    'message': {'header': 'Nie udało się!',
                                'body': 'Podane stare hasło nie jest poprawne!'}}
        
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}}
    

def update_expense(expense_id, amount, category, date, account, description):
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB["Expenses"]

        expense_id = ObjectId(expense_id)

        expenses_collection.find_one_and_update({'_id': expense_id}, {'$set': {'amount': amount, 'category': category, 'date_at': date, 'account': account, 'description': description}})

        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie zaktualizowano wydatek!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 
    

def update_category(email, category_old, category_new):
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB['Expenses']
        users_collection = DB['Users']

        users_collection.update_one({'email': email, 'categories': category_old}, {'$set': {'categories.$': category_new}})

        expenses_collection.update_many({'email': email, 'category': category_old}, {'$set': {'category': category_new}})

        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie zaktualizowano kategorię!'}}

    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}}
    

def update_account(email, old_account_name, new_account_name, balance, cyclical, income_amount = False, income_day = False):
    try:
        DB = app.db_connection.home_budget_app
        accounts_collection = DB['Accounts']

        if new_account_name != old_account_name and accounts_collection.find_one({'email': email, 'name': new_account_name}):
            return {'result': 'danger',
                'message': {'header': 'Nie udało się.',
                            'body': 'Konto o podanej nazwie istnieje już na Twoim koncie. Spróbuj ponownie, używając innej nazwy.'}}
        
        next_income_date = datetime(datetime.now().year, datetime.now().month, int(income_day))

        if not next_income_date.day > datetime.now().day:
            next_income_date = next_income_date + relativedelta(months=1)
        
        accounts_collection.update_one({'email': email, 'name': old_account_name}, {'$set': {'name': new_account_name, 'balance': balance, 'income_active': cyclical, 'income': income_amount, 'next_income_date': next_income_date}})
        
        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie dodano konto!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 
    

#! DELETE METHODS
    
def delete_user_account(email, password):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB['Users']
        expenses_collection = DB['Expenses']

        current_password = users_collection.find_one({'email': email}, projection={'password':True})['password']

        if check_password_hash(current_password, password):
            users_collection.find_one_and_delete({'email': email})
            expenses_collection.delete_many({'email': email})

            return {'result': 'success',
                    'message': {'header': 'Konto usunięte pomyślnie!',
                                'body': f'Pomyślnie usunięto konto {email}!'}}
        else:
            return {'result': 'danger',
                    'message': {'header': 'Niepoprawne hasło!',
                                'body': 'Podałeś niepoprawne hasło!'}}
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 

    
def delete_expense(expense_id):
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB["Expenses"]

        expense_id = ObjectId(expense_id)

        expenses_collection.find_one_and_delete({'_id': expense_id})

        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie usunięto wydatek!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 


def delete_category(email, category):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB['Users']
        expenses_collection = DB['Expenses']

        users_collection.update_one({'email': email}, {'$pull': {'categories': category}})
        expenses_collection.delete_many({'email': email, 'category': category})

        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie usunięto kategorię!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 
    

def delete_account(email, account_name):
    try:
        DB = app.db_connection.home_budget_app
        accounts_collection = DB['Accounts']

        accounts_collection.delete_one({'email': email, 'name': account_name})
        
        return {'result': 'success',
                'message': {'header': 'Powodzenie!',
                            'body': 'Pomyślnie usunięto konto!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}}


#! GET METHODS


def authenticate_user(email, password):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]

        user = users_collection.find_one({'email': email})

        if user is not None:
            if check_password_hash(user.get('password'), password) and user.get('status') == 'active':
                cyclical_budget_update(email)
                return {'result': 'success',
                        'user': parse_json(user),
                        'message': {'header': 'Dzień dobry!',
                                    'body': 'Zalogowano pomyślnie :)'}}
            elif user.get('status') != 'active':
                return {'result': 'danger',
                        'message': {'header': 'Oops :(',
                                    'body': 'Użytkownik nie jest aktywny.'}}
            else:
                return {'result': 'danger',
                        'message': {'header': 'Oops :(',
                                    'body': 'Podane hasło nie jest poprawne.'}}
        else:
            return {'result': 'danger',
                    'message': {'header': 'Oops :(',
                                'body': 'Użytkownik o podanym mailu nie istnieje.'}} 
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}}


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
        accounts_collection = DB["Accounts"]
        accounts = accounts_collection.find({'email': email}, projection={'balance':True, 'name': True, 'income_active': True, 'income': True, 'next_income_date': True})
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

        if expense_count != 0:
            expense_sum = expenses_collection.aggregate([{'$match': {'email': email}}, {'$group': {'_id': None, 'sum': {'$sum': '$amount'}}}])
            expense_sum = parse_json(expense_sum)[0]['sum']
        else:
            expense_sum = 0


        # ! DO PRZEPISANIA NA NOWĄ KOLEKCJĘ ACCOUNTS

        # account_count = users_collection.aggregate([{'$match': {'email': email}}, {'$project': {'count': {'$size': '$accounts'}}}])
        # account_count = parse_json(account_count)[0]['count']

        # if account_count != 0:
        #     account_sum = users_collection.find({'email': email}, {'sum': {'$sum': '$accounts.current_balance'}})
        #     account_sum = parse_json(account_sum)[0]['sum']
        # else:
        #     account_sum = None


        #TODO: kalkulowanie sredniej wydatków za ostatnie 30 dni

        return {
            'member_from': member_from,
            'expense_count': expense_count,
            'expense_sum': round(expense_sum, 2),
            'account_count': 0,
            'accounts_sum': 0,
            'expense_avg': 0
        }


    except Exception as e:
        return e
    

def cyclical_budget_update(email):
    try:
        DB = app.db_connection.home_budget_app
        accounts_collection = DB["Accounts"]

        accounts = accounts_collection.find({'email': email})
        accounts = parse_json(accounts)

        for account in accounts:
            print(account)
            income_date = datetime.strptime(account['next_income_date']['$date'], "%Y-%m-%dT%H:%M:%SZ")
            
            if datetime.now() >= income_date:
                print('DODAWANIE SRODKOW DO KONTA')
                income = float(account['income'])
                name = account['name']
                next_income_date = income_date + relativedelta(months=1)
                accounts_collection.find_one_and_update({'email': email, 'name': name}, {'$inc': {'balance': income}, '$set': {'next_income_date': next_income_date}})

    except Exception as e:
        print(e)

