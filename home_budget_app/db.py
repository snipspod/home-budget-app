from pymongo import ASCENDING, DESCENDING
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from home_budget_app.utils import parse_json
from bson import ObjectId


def create_user(name, email, password, password_confirm):
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
    }

    if password is not password_confirm:
        return {'result': 'danger',
                'message': {'header': 'Niepowodzenie!',
                            'body': 'Podane hasła nie są zgodne!'}}

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
    
 
def add_single_expense(email, amount, date, account_id, category_id, description):
    DB = app.db_connection.home_budget_app
    expenses_collection = DB["Expenses"]
    accounts_collection = DB['Accounts']

    category_id = ObjectId(category_id)
    account_id = ObjectId(account_id)

    account_details = accounts_collection.find_one({'_id': account_id}, projection={'balance': True, 'name': True})

    if amount > account_details['balance']:
        return {'result': 'danger',
                'message': {'header': 'Nie udało się!',
                            'body': f'Nie udało się dodać wydatku {description}. Na koncie {account_details['name']} nie ma wystarczająco środków!'}}

    expense = {
        'email': email,
        'description': description,
        'category_id': category_id,
        'account_id': account_id,
        'amount': amount,
        'date_at': date,
        'date_submitted': datetime.now(),
    }
    
    try:
        expenses_collection.insert_one(expense)
        accounts_collection.update_one({'_id': account_id}, {'$inc': {'balance': -(amount)}})
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
        category_collection = DB['Categories']

        category_collection.insert_one({'name': category, 'email': email})

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
    

def add_budget(email, name, amount, assoc_categories):
    try:
        DB = app.db_connection.home_budget_app
        budgets_collection = DB['Budgets']

        category_sum = 0
        for category in assoc_categories:
            category_sum += category['amount']
            category['amount'] = round(category['amount'], 2)

        if round(category_sum,2) != round(amount, 2):
            return {'result': 'danger',
                'message': {'header': 'Błąd!',
                            'body': f'Podany kwota budżetu: {amount}zł. Suma kategorii: {round(category_sum, 2)}zł.'}}
        
        if budgets_collection.find_one({'name': name}):
            return {'result': 'danger',
                'message': {'header': 'Nie udało się dodać budżetu!',
                            'body': f'Posiadasz już budżet o nazwie {name}'}}
        
        budget = {
            'email': email,
            'name': name,
            'amount': amount,
            'spent': 0,
            'assoc_categories': assoc_categories
        }
        
        budgets_collection.insert_one(budget)
        return {'result': 'success',
                'message': {'header': 'Wszystko OK!',
                            'body': 'Wsysztko spoko mordziaty'}}

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
    

def update_expense(expense_id, amount, category_id, date, account_id, description):
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB["Expenses"]
        accounts_collection = DB['Accounts']

        expense_id = ObjectId(expense_id)
        account_id = ObjectId(account_id)
        category_id = ObjectId(category_id)

        old_expense_amount = expenses_collection.find_one({'_id': expense_id})['amount']

        account_difference = old_expense_amount - amount

        accounts_collection.find_one_and_update({'_id': account_id}, {'$inc': {'balance': account_difference}})
        

        expenses_collection.find_one_and_update({'_id': expense_id}, {'$set': {'amount': amount, 'category_id': category_id, 'date_at': date, 'account_id': account_id, 'description': description}})

        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie zaktualizowano wydatek!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 
    

def update_category(category_id, category_new):
    try:
        DB = app.db_connection.home_budget_app
        categories_collection = DB['Categories']

        category_id = ObjectId(category_id)

        categories_collection.update_one({'_id': category_id}, {'$set': {'name': category_new}})

        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie zaktualizowano kategorię!'}}

    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}}
    

def update_account(email, account_id, new_account_name, balance, cyclical, income_amount = False, income_day = False):
    try:
        DB = app.db_connection.home_budget_app
        accounts_collection = DB['Accounts']

        account_id = ObjectId(account_id)

        old_account_name = accounts_collection.find_one({'_id': account_id})['name']

        if new_account_name != old_account_name and accounts_collection.find_one({'email': email, 'name': new_account_name}):
            return {'result': 'danger',
                'message': {'header': 'Nie udało się.',
                            'body': 'Konto o podanej nazwie istnieje już na Twoim koncie. Spróbuj ponownie, używając innej nazwy.'}}
        
        next_income_date = datetime(datetime.now().year, datetime.now().month, int(income_day))

        if not next_income_date.day > datetime.now().day:
            next_income_date = next_income_date + relativedelta(months=1)
        
        accounts_collection.update_one({'_id': account_id}, {'$set': {'name': new_account_name, 'balance': balance, 'income_active': cyclical, 'income': income_amount, 'next_income_date': next_income_date}})
        
        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie zaktualizowano dane o koncie!'}}
    
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
        accounts_collection = DB['Accounts']
        budgets_collection = DB['Budgets']
        categories_collection = DB['Categories']

        current_password = users_collection.find_one({'email': email}, projection={'password':True})['password']

        if check_password_hash(current_password, password):
            users_collection.find_one_and_delete({'email': email})
            expenses_collection.delete_many({'email': email})
            accounts_collection.delete_many({'email': email})
            budgets_collection.delete_many({'email': email})
            categories_collection.delete_many({'email': email})

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


def delete_category(category_id):
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB['Expenses']
        categories_collection = DB['Categories']

        category_id = ObjectId(category_id)

        categories_collection.delete_one({'_id': category_id})
        expenses_collection.delete_many({'category_id': category_id})

        return {'result': 'success',
                'message': {'header': 'Wohoo!',
                            'body': 'Pomyślnie usunięto kategorię i wydatki z tej kategorii!'}}
    
    except Exception as e:
        return {'result': 'danger',
                'message': {'header': 'Nieznany błąd!',
                            'body': e}} 
    

def delete_account(account_id):
    try:
        DB = app.db_connection.home_budget_app
        accounts_collection = DB['Accounts']
        expenses_collection = DB['Expenses']

        account_id = ObjectId(account_id)

        accounts_collection.delete_one({'_id': account_id})
        expenses_collection.delete_many({'_id': account_id})
        
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
        categories_collection = DB["Categories"]
        categories = categories_collection.find({'email': email})
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
    
def get_user_expenses(email, limit = 9999):
    """Returns user expenses. Amount of returned documents can be limited by specifying second **parameter**."""
    
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB["Expenses"]
        
        expenses = expenses_collection.aggregate(
            [{'$match': {'email': email}}, {'$limit': limit}, {'$sort': {'data_at': -1}}, {'$lookup': {'from': 'Categories', 'localField': 'category_id', 'foreignField': '_id', 'as': 'category'}}, {'$lookup': {'from': 'Accounts', 'localField': 'account_id', 'foreignField': '_id', 'as': 'account'}}, {'$project': {'amount': 1, 'date_at': 1, 'date_submitted': 1, 'description': 1, 'category_id': 1, 'category': {'$first': '$category.name'}, 'account_id': 1, 'account_name': {'$first': '$account.name'}}}]
            )

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

