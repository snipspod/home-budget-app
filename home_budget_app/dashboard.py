from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
import datetime
from home_budget_app.auth import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/', methods=('GET',))
@login_required
def index():

    from home_budget_app.db import get_user_categories, get_user_accounts, get_user_expenses
    categories = get_user_categories(g.user['email'])
    accounts = get_user_accounts(g.user['email'])
    expenses = get_user_expenses(g.user['email'])

    print(expenses)


    return render_template('dashboard/index.html', categories=categories, accounts=accounts, expenses=expenses)

@bp.route('/', methods=("POST",))
@login_required
def add_single_expense():
    from home_budget_app.db import add_single_expense

    back = request.referrer
    if request.method == 'POST':
        amount = float(request.form['amount'].replace(',','.'))
        category = request.form['category']
        dateStr = request.form['date']
        account = request.form['account']
        description = request.form['description']

        date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")

        error = None

        try:
            add_single_expense(
                email = g.user['email'],
                amount = amount,
                date = date,
                account = account,
                category = category,
                description = description
            )
        except Exception as e:
            error = e

        if error is None:
            return redirect(back)

        flash(error, 'warning')
