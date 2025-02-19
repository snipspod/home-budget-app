from pymongo import ASCENDING, DESCENDING
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from home_budget_app.utils import parse_json, last_day_of_month
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
    }

    if password != password_confirm:
        return {'result': 'danger',
                'message': {'header': 'Niepowodzenie!',
                            'body': 'Podane hasła nie są zgodne!'}}

    if users_collection.find_one({'email': email}) is None:
        try:
            users_collection.insert_one(user)
            return {'result': 'success',
                    'message': {'header': 'Udało się!',
                                'body': 'Użytkownik pomyślnie zarejestrowany!'}}
        except Exception as e:
            return {'result': 'danger',
                    'message': {'header': 'Nieznany błąd',
                                'body': e}}
    else:
        return {'result': 'danger',
                'message': {'header': 'Niepowodzenie',
                            'body': 'Użytkownik z takim mailem już istnieje!'}}
    
 
def add_single_expense(email, amount, date, account_id, category_id, description):
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB["Expenses"]
        accounts_collection = DB['Accounts']

        category_id = ObjectId(category_id)
        account_id = ObjectId(account_id)

        account_details = accounts_collection.find_one({'_id': account_id}, projection={'balance': True, 'name': True})

        if amount > account_details['balance']:
            return {'result': 'danger',
                    'message': {'header': 'Nie udało się!',
                                'body': f'Nie udało się dodać wydatku {description}. Na koncie {account_details["name"]} nie ma wystarczająco środków!'}}

        expense = {
            'email': email,
            'description': description,
            'category_id': category_id,
            'account_id': account_id,
            'amount': amount,
            'date_at': date,
            'date_submitted': datetime.now(),
        }
    
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
    

def add_budget(email, name, amount, assoc_categories, budget_month):
    try:
        DB = app.db_connection.home_budget_app
        budgets_collection = DB['Budgets']

        category_sum = 0
        for category in assoc_categories:
            category_sum += category['amount']
            category['amount'] = round(category['amount'], 2)
            category['category_id'] = ObjectId(category['category_id'])
            category['spent'] = 0

        if round(category_sum,2) != round(amount, 2):
            return {'result': 'danger',
                'message': {'header': 'Błąd!',
                            'body': f'Podany kwota budżetu: {amount}zł. Suma kategorii: {round(category_sum, 2)}zł.'}}
        
        if budget_month > 12 or budget_month < 1:
            return {'result': 'danger',
                'message': {'header': 'Błąd!',
                            'body': f'W roku nie istnieje miesiąc {budget_month}'}}
        
        budget_month = datetime(datetime.now().year, budget_month, 1)
        
        budget = {
            'email': email,
            'name': name,
            'amount': amount,
            'spent': 0,
            'assoc_categories': assoc_categories,
            'budget_month': budget_month
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
        budgets_collection = DB['Budgets']

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
    
def update_budget(budget_id, budget_month, amount, name, assoc_categories):
    try:
        DB = app.db_connection.home_budget_app
        budgets_collection = DB['Budgets']

        budget_id = ObjectId(budget_id)

        category_sum = 0
        for category in assoc_categories:
            category_sum += category['amount']
            category['amount'] = round(category['amount'], 2)
            category['category_id'] = ObjectId(category['category_id'])
            category['spent'] = 0

        if round(category_sum,2) != round(amount, 2):
            return {'result': 'danger',
                'message': {'header': 'Błąd!',
                            'body': f'Podany kwota budżetu: {amount}zł. Suma kategorii: {round(category_sum, 2)}zł.'}}
        
        if budget_month > 12 or budget_month < 1:
            return {'result': 'danger',
                'message': {'header': 'Błąd!',
                            'body': f'W roku nie istnieje miesiąc {budget_month}'}}
        
        budget_month = datetime(datetime.now().year, budget_month, 1)

        budgets_collection.update_one({'_id': budget_id}, {'$set': {'assoc_categories': assoc_categories, 'budget_month': budget_month, 'name': name, 'amount': amount}})


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
    
def delete_budget(budget_id):
    try:
        DB = app.db_connection.home_budget_app
        budgets_collection = DB['Budgets']

        budget_id = ObjectId(budget_id)

        budgets_collection.delete_one({'_id': budget_id})
        
        return {'result': 'success',
                'message': {'header': 'Powodzenie!',
                            'body': 'Pomyślnie usunięto budżet!'}}
    
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
            if check_password_hash(user.get('password'), password):
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
        accounts = accounts_collection.aggregate([{'$match':{'email':email}},{'$project':{'balance':{'$round':['$balance',2]},'income_active':1,'income':1,'name':1,'next_income_date':1}}])
        return parse_json(accounts)
    except Exception as e:
        return e
    
def get_user_expenses(email, limit = 9999):
    """Returns user expenses. Amount of returned documents can be limited by specifying second **parameter**."""
    
    try:
        DB = app.db_connection.home_budget_app
        expenses_collection = DB["Expenses"]
        
        expenses = expenses_collection.aggregate(
            [{'$match': {'email': email}}, {'$sort':{'date_at': -1}}, {'$limit': limit}, {'$lookup': {'from': 'Categories', 'localField': 'category_id', 'foreignField': '_id', 'as': 'category'}}, {'$lookup': {'from': 'Accounts', 'localField': 'account_id', 'foreignField': '_id', 'as': 'account'}}, {'$project': {'amount': 1, 'date_at': 1, 'date_submitted': 1, 'description': 1, 'category_id': 1, 'category': {'$first': '$category.name'}, 'account_id': 1, 'account_name': {'$first': '$account.name'}}}]
            )
        return parse_json(expenses)
    except Exception as e:
        return e
    
def get_user_budgets(email):
    try:
        DB = app.db_connection.home_budget_app
        budgets_collection = DB['Budgets']
        expenses_collection = DB['Expenses']
        date_now = datetime(datetime.now().year, datetime.now().month, 1)
        date_last = last_day_of_month(date_now)

        expenses = parse_json(expenses_collection.aggregate([{'$match':{'email': email,'date_at':{'$gte':date_now,'$lte':date_last}}},{'$group':{'_id':'$category_id','sum':{'$sum':'$amount'}}},{'$lookup':{'from':'Categories','localField':'_id','foreignField':'_id','as':'result'}},{'$unwind':{'path':'$result'}},{'$project':{'sum':1,'_id':0,'category_id':'$result._id', 'category_name':'$result.name'}}]))
        
        budgets = parse_json(budgets_collection.aggregate([{'$match':{'email':email, 'budget_month': date_now}},{'$lookup':{'from':'Categories','localField':'assoc_categories.category_id','foreignField':'_id','as':'category_details'}},{'$project':{'name':1,'amount':1,'budget_month':{'$month': '$budget_month'},'assoc_categories':{'$map':{'input':'$assoc_categories','in':{'$let':{'vars':{'m':{'$arrayElemAt':[{'$filter':{'input':'$category_details','cond':{'$eq':['$$mb._id','$$this.category_id']},'as':'mb'}},0]}},'in':{'$mergeObjects':['$$this',{'name':'$$m.name'}]}}}}}}}]))

        for budget in budgets:
            budget['spent'] = 0
            for category in budget['assoc_categories']:
                category['spent'] = 0
                for expense in expenses:
                    if ObjectId(category['category_id']['$oid']) == ObjectId(expense['category_id']['$oid']):
                        category['spent'] = expense['sum']
                        budget['spent'] += expense['sum']

        return parse_json(budgets)
    except Exception as e:
        return e
    
def get_historical_user_budgets(email):
    try:
        DB = app.db_connection.home_budget_app
        budgets_collection = DB['Budgets']
        expenses_collection = DB['Expenses']
        current_month = datetime(datetime.now().year, datetime.now().month, 1) - relativedelta(days=1)

        expenses = parse_json(expenses_collection.aggregate([{'$match':{'email':email,'date_at':{'$lte':current_month}}},{'$group':{'_id':{'year':{'$year':'$date_at'},'month':{'$month':'$date_at'},'category_id':'$category_id'},'sum':{'$sum':'$amount'}}},{'$project':{'category_id':'$_id.category_id','expense_date':{'$concat':[{'$toString':'$_id.year'},'-',{'$cond':[{'$lte':['$_id.month',9]},{'$concat':['0',{'$substr':['$_id.month',0,2]}]},{'$substr':['$_id.month',0,2]}]}]},'sum':1,'_id':0}}]))
        
        budgets = parse_json(budgets_collection.aggregate([{'$match':{'email':email, 'budget_month': {'$lte': current_month}}},{'$lookup':{'from':'Categories','localField':'assoc_categories.category_id','foreignField':'_id','as':'category_details'}},{'$project':{'email':1,'name':1,'amount':1,'budget_date': {'$dateToString': {'date': '$budget_month', 'format': '%Y-%m'}},'assoc_categories':{'$map':{'input':'$assoc_categories','in':{'$let':{'vars':{'m':{'$arrayElemAt':[{'$filter':{'input':'$category_details','cond':{'$eq':['$$mb._id','$$this.category_id']},'as':'mb'}},0]}},'in':{'$mergeObjects':['$$this',{'name':'$$m.name'}]}}}}}}},{'$group':{'_id': "$budget_date",'budgets': {'$addToSet': "$$ROOT",},},},{'$project':{'date': "$_id",'_id': 0,'budgets': 1,},},{'$sort':{'date': 1},}]))

        for month in budgets:
            for budget in month['budgets']:
                budget['spent'] = 0
                for category in budget['assoc_categories']:
                    category['spent'] = 0
                    for expense in expenses:
                        if ObjectId(category['category_id']['$oid']) == ObjectId(expense['category_id']['$oid']) and expense['expense_date'] == budget['budget_date']:
                            category['spent'] = expense['sum']
                            # print(category['spent'])
                            budget['spent'] += expense['sum']
        print(budgets)

        return parse_json(budgets)
    except Exception as e:
        return e
    
def get_user_statistics(email):
    try:
        DB = app.db_connection.home_budget_app
        users_collection = DB["Users"]
        expenses_collection = DB["Expenses"]
        accounts_collection = DB["Accounts"]

        month_start = datetime(datetime.now().year, datetime.now().month, 1)
        today = datetime.now()

        member_from = users_collection.find_one({'email': email}, projection={'created_at': True})['created_at']
        print(member_from)

        expense_count = expenses_collection.count_documents({'email': email})

        if expense_count != 0:
            expense_sum = expenses_collection.aggregate([{'$match': {'email': email}}, {'$group': {'_id': None, 'sum': {'$sum': '$amount'}}}])
            expense_sum = parse_json(expense_sum)[0]['sum']
        else:
            expense_sum = 0


        account_count = accounts_collection.count_documents({'email': email})

        if account_count != 0:
            account_sum = accounts_collection.aggregate([{'$match': {'email': email}}, {'$group': {'_id': 1, 'sum': {'$sum': '$balance'}}}])
            account_sum = parse_json(account_sum)[0]['sum']
        else:
            account_sum = None
        
        expense_avg = expenses_collection.aggregate([{'$match':{'date_at':{'$gte':month_start,'$lte':today}, 'email': email}},{'$group':{'_id':'$email','expense_sum':{'$sum':'$amount'}}},{'$project':{'_id':0,'email':'$_id','average_expense':{'$divide':['$expense_sum',{'$dayOfMonth':'$$NOW'}]}}}])
        expense_avg = round(parse_json(expense_avg)[0]['average_expense'],2)

        return {
            'member_from': member_from,
            'expense_count': expense_count,
            'expense_sum': round(expense_sum, 2),
            'account_count': account_count,
            'accounts_sum': account_sum,
            'expense_avg': expense_avg
        }


    except Exception as e:
        return e
    

def get_last_month_expense_sum_by_category(email):
    try: 
        DB = app.db_connection.home_budget_app
        expenses_collection = DB['Expenses']
        date_now = datetime(datetime.now().year, datetime.now().month, 1)
        date_last = last_day_of_month(date_now)

        expenses = expenses_collection.aggregate([{'$match':{'email': email,'date_at':{'$gte':date_now,'$lte':date_last}}},{'$group':{'_id':'$category_id','sum':{'$sum':'$amount'}}},{'$lookup':{'from':'Categories','localField':'_id','foreignField':'_id','as':'result'}},{'$unwind':{'path':'$result'}},{'$project':{'sum':1,'_id':0,'name':'$result.name'}}])
        return parse_json(expenses)

    except Exception as e:
        return e
    
def get_expense_sum_per_month(email):
    try: 
        DB = app.db_connection.home_budget_app
        expenses_collection = DB['Expenses']
        oldest_date = datetime(datetime.now().year - 1, datetime.now().month, 1)

        sum_per_month = parse_json(expenses_collection.aggregate([{'$match':{'email':email, 'date_at': {'$gte': oldest_date}}},{'$project':{'amount':1,'month_at':{'$dateFromParts':{'year':{'$year':'$date_at'},'month':{'$month':'$date_at'}}}}},{'$group':{'_id':'$month_at','spent':{'$sum':'$amount'}}},{'$sort': {'_id': 1}},{'$project':{'_id':0,'month':{'$dateToString': {'format': '%B %Y','date': '$_id'}},'spent':1}}]))

        lookup_table = {
            'January': 'Styczeń',
            'February': 'Luty',
            'March': 'Marzec',
            'April': 'Kwiecień',
            'May': 'Maj',
            'June': 'Czerwiec',
            'July': 'Lipiec',
            'August': 'Sierpień',
            'September': 'Wrzesień',
            'October': 'Pażdziernik',
            'November': 'Listopad',
            'Decebmer': 'Grudzień'
        }

        for month in sum_per_month:
            for key in lookup_table:
                month['month'] = month['month'].replace(key, lookup_table[key])

        return sum_per_month

    except Exception as e:
        return e
    

def get_budgets_realization(email):
    try: 
        DB = app.db_connection.home_budget_app
        budgets_collection = DB['Budgets']
        expenses_collection = DB['Expenses']

        budgets = parse_json(budgets_collection.aggregate([{'$match':{'email':email}},{'$project':{'_id':0,'name':1,'assoc_categories':1,'amount': 1,'budget_date':{'$dateToString':{'date':'$budget_month','format':'%Y-%m'}}}},{'$group':{'_id':'$budget_date','budgets':{'$addToSet':'$$ROOT'}}},{'$project':{'budgets':1,'date':'$_id','_id':0}}]))

        expenses = parse_json(expenses_collection.aggregate([{'$match':{'email':email}},{'$group':{'_id':{'year':{'$year':'$date_at'},'month':{'$month':'$date_at'},'category_id':'$category_id'},'sum':{'$sum':'$amount'}}},{'$project':{'category_id':'$_id.category_id','expense_date':{'$concat':[{'$toString':'$_id.year'},'-',{'$cond':[{'$lte':['$_id.month',9]},{'$concat':['0',{'$substr':['$_id.month',0,2]}]},{'$substr':['$_id.month',0,2]}]}]},'sum':1,'_id':0}}]))

        for month in budgets:
            for budget in month['budgets']:
                budget['spent'] = 0
                for category in budget['assoc_categories']:
                    for expense in expenses:
                        if ObjectId(category['category_id']['$oid']) == ObjectId(expense['category_id']['$oid']) and expense['expense_date'] == budget['budget_date']:
                            budget['spent'] += expense['sum']
                budget['label'] = f'{budget['spent']} / {budget['amount']} zł'
                budget['realization'] = budget['spent']/budget['amount']

        return parse_json(budgets)
    except Exception as e:
        return e

    
    

def cyclical_budget_update(email):
    try:
        accounts_collection = app.db_connection.home_budget_app["Accounts"]

        accounts = parse_json(accounts_collection.find({'email': email}))

        for account in accounts:
            income_date = datetime.strptime(account['next_income_date']['$date'], "%Y-%m-%dT%H:%M:%SZ")
            
            if datetime.now() >= income_date:
                income = float(account['income'])
                name = account['name']
                next_income_date = income_date + relativedelta(months=1)
                accounts_collection.find_one_and_update({'email': email, 'name': name}, {'$inc': {'balance': income}, '$set': {'next_income_date': next_income_date}})

    except Exception as e:
        return e