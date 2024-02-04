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

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('/', methods=('GET',))
@login_required
def index():
    from home_budget_app.db import get_user_accounts
    from datetime import datetime

    accounts = get_user_accounts(g.user['email'])
    
    for account in accounts:
        income_day = datetime.strptime(account['next_income_date']['$date'], "%Y-%m-%dT%H:%M:%SZ").day
        account['income_day'] = income_day

    return render_template('accounts.html', accounts=accounts)

@bp.route('/update-account', methods=('POST',))
@login_required
def update_account():
    back = request.referrer

    from home_budget_app.db import update_account

    account_id = request.form.get('account_id')
    new_account_name = request.form.get('new_account_name')
    balance = float(request.form.get('balance_new').replace(',','.'))
    cyclical = True if request.form.get('is_cyclical') else False
    income_amount = float(request.form.get('income_amount'))
    income_day = request.form.get('income_day')

    db_result = update_account(g.user['email'], account_id, new_account_name,balance, cyclical, income_amount, income_day)
        
    flash(db_result['message'], db_result['result'])
    return redirect(back)

@bp.route('/delete-account', methods=('POST',))
@login_required
def delete_account():
    back = request.referrer
    from home_budget_app.db import delete_account

    account_id = request.form.get('account_id')

    db_result = delete_account(account_id)
        
    flash(db_result['message'], db_result['result'])
    
    return redirect(back)

@bp.route('/add-account', methods=('POST',))
@login_required
def add_account():
    back = request.referrer

    from home_budget_app.db import add_account

    account_name = request.form.get('account_name')
    start_balance = float(request.form.get('start_balance').replace(',','.'))
    cyclical = True if request.form.get('is_cyclical') else False
    print(request.form.get('income_amount'))
    income_amount = float(request.form.get('income_amount'))
    income_amount = 0
    income_day = request.form.get('income_day')

    db_result = add_account(g.user['email'], account_name, start_balance, cyclical, income_amount, income_day)
        

    flash(db_result['message'], db_result['result'])
    return redirect(back)