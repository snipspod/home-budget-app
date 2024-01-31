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

    accounts = get_user_accounts(g.user['email'])

    return render_template('accounts.html', accounts=accounts)

@bp.route('/update-account', methods=('POST',))
@login_required
def update_account():
    back = request.referrer

    from home_budget_app.db import update_account

    if request.form.get('is_cyclical'):
        old_account_name = request.form.get('old_account_name')
        new_account_name = request.form.get('new_account_name')
        start_balance = float(request.form.get('balance_new').replace(',','.'))
        income_amount = float(request.form['income_amount'])
        income_day = request.form['income_day']
        db_result = update_account(g.user['email'], old_account_name, new_account_name, start_balance, income_amount, income_day)
    else:
        old_account_name = request.form.get('old_account_name')
        new_account_name = request.form.get('new_account_name')
        start_balance = float(request.form.get('balance_new').replace(',','.'))
        db_result = update_account(g.user['email'], old_account_name, new_account_name, start_balance)
        
    flash(db_result['message'], db_result['result'])
    return redirect(back)

@bp.route('/delete-account', methods=('POST',))
@login_required
def delete_account():
    back = request.referrer
    from home_budget_app.db import delete_account

    account_name = request.form.get('account')

    db_result = delete_account(g.user['email'], account_name)
        
    flash(db_result['message'], db_result['result'])
    
    return redirect(back)

@bp.route('/add-account', methods=('POST',))
@login_required
def add_account():
    back = request.referrer

    from home_budget_app.db import add_account

    if request.form.get('is_cyclical'):
        account_name = request.form.get('account_name')
        start_balance = float(request.form.get('start_balance').replace(',','.'))
        income_amount = float(request.form['income_amount'])
        income_day = request.form['income_day']
        db_result = add_account(g.user['email'], account_name, start_balance, income_amount, income_day)
    else:
        account_name = request.form.get('account_name')
        start_balance = float(request.form.get('start_balance').replace(',','.'))
        db_result = add_account(g.user['email'], account_name, start_balance)
        

    flash(db_result['message'], db_result['result'])
    return redirect(back)