from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

from home_budget_app.auth import login_required

bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@bp.route('/', methods=('GET',))
@login_required
def index():
    return render_template('expenses/expenses.html')


@bp.route('/history', methods=('GET',))
@login_required
def expense_history():
        from home_budget_app.db import get_user_expenses, get_user_categories, get_user_accounts
        
        expenses = get_user_expenses(g.user['email'])
        categories = get_user_categories(g.user['email'])
        accounts = get_user_accounts(g.user['email'])

        return render_template('expenses/expenses_history.html', expenses=expenses, categories=categories, accounts=accounts)

@bp.route('/', methods=('POST',))
@login_required
def update_expense():

    from datetime import datetime
    from home_budget_app.db import update_expense
      
    back = request.referrer

    expense_id = request.form['expense_id']
    amount = float(request.form['amount'].replace(',','.'))
    category = request.form['category']
    date = datetime.strptime(request.form['date'], "%Y-%m-%d")
    account = request.form['account']
    description = request.form['description'].strip()

    db_result = update_expense(expense_id, amount, category, date, account, description)

    flash(db_result['message'], db_result['result'])

    print(expense_id)
    return redirect(back)