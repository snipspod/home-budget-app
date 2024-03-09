from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app
)
from datetime import datetime
from home_budget_app.auth import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/', methods=('GET',))
@login_required
def index():

    from home_budget_app.db import get_user_categories, get_user_accounts, get_user_expenses, get_last_month_expense_sum_by_category

    categories = get_user_categories(g.user['email'])
    accounts = get_user_accounts(g.user['email'])
    expenses = get_user_expenses(g.user['email'], 5)
    date = datetime.today().strftime('%Y-%m-%d')
    categories_spent = get_last_month_expense_sum_by_category(g.user['email'])
    print(categories_spent)
    return render_template('dashboard.html', categories=categories, accounts=accounts, expenses=expenses, date=date, categories_spent=categories_spent)

@bp.route('/add-expense', methods=("POST",))
@login_required
def add_single_expense():
    from home_budget_app.db import add_single_expense

    back = request.referrer
    if request.method == 'POST':
        amount = float(request.form['amount'].replace(',','.'))
        category_id = request.form['category']
        date = datetime.strptime(request.form['date'], "%Y-%m-%d")
        account_id = request.form['account']
        description = request.form['description'].strip()

        db_result = add_single_expense(
                email = g.user['email'],
                amount = amount,
                date = date,
                account_id = account_id,
                category_id = category_id,
                description = description
        )
        flash(db_result['message'], db_result['result'])
        return redirect(back)

        
