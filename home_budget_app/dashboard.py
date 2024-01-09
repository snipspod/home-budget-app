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

    from home_budget_app.db import get_user_categories, get_user_accounts
    categories = get_user_categories(g.user['email'])
    accounts = get_user_accounts(g.user['email'])
    print(accounts)

    return render_template('dashboard/index.html', categories=categories, accounts=accounts)

@bp.route('/', methods=("POST",))
@login_required
def add_single_expense():

    #! PAMIĘTAĆ O PRZEKONWERTOWANIU AMOUNT NA DOUBLE / ZAMIENIĆ PRZECINEK NA KROPKĘ
    from home_budget_app.db import add_single_expense

    back = request.referrer
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        dateStr = request.form['date']
        account = request.form['account']
        comment = request.form['comment']

        date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")

        print(amount)

        error = None

        # try:
        #     transaction = add_single_expense(
        #         email = g.user['email'],
        #         amount = amount,
        #         transactionType = operation,
        #         date = date,
        #         account = account,
        #         category = 'test',
        #         description = comment
        #     )
        # except Exception as e:
        #     error = e

        if error is None:
            return redirect(back)

        flash(error, 'warning')
