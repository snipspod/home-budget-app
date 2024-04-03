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

@bp.route('/history', methods=('GET',))
@login_required
def expense_history():
        from home_budget_app.db import get_user_expenses, get_user_categories, get_user_accounts
        
        expenses = get_user_expenses(g.user['email'])
        categories = get_user_categories(g.user['email'])
        accounts = get_user_accounts(g.user['email'])

        return render_template('expenses_history.html', expenses=expenses, categories=categories, accounts=accounts)


@bp.route('/add', methods=('GET',))
@login_required
def expense_add():
     
     from home_budget_app.db import get_user_accounts, get_user_categories
     from datetime import datetime

     categories = get_user_categories(g.user['email'])
     accounts = get_user_accounts(g.user['email'])
     date = datetime.now().strftime("%Y-%m-%d")

     return render_template('expenses_add.html', accounts=accounts, categories=categories, date=date)


@bp.route('/submit-expenses', methods=('POST',))
def add_multiple_expenses():
    from home_budget_app.db import add_single_expense
    from datetime import datetime
    back = request.referrer


    for amount, description, category, account, date in zip(request.form.getlist('amount'),
                                                            request.form.getlist('description'),
                                                            request.form.getlist('category'),
                                                            request.form.getlist('account'),
                                                            request.form.getlist('date')):
          amount = float(amount.replace(',','.'))
          description = description.strip()
          date = datetime.strptime(date, "%Y-%m-%d")
          db_result = add_single_expense(g.user['email'], amount, date, account, category, description)
          flash(db_result['message'], db_result['result'])

    return redirect(back)


@bp.route('/update', methods=('POST',))
@login_required
def update_expense():

    from datetime import datetime
    from home_budget_app.db import update_expense
      
    back = request.referrer

    expense_id = request.form.get('expense_id')
    amount = float(request.form.get('amount').replace(',','.'))
    category_id = request.form.get('category')
    date = datetime.strptime(request.form.get('date'), "%Y-%m-%d")
    account_id = request.form.get('account')
    description = request.form.get('description').strip()

    db_result = update_expense(expense_id, amount, category_id, date, account_id, description)

    flash(db_result['message'], db_result['result'])

    return redirect(back)



@bp.route('/delete', methods=('POST',))
@login_required
def delete_expense():

    from home_budget_app.db import delete_expense
    back = request.referrer

    expense_id = request.form.get('expense_id')

    db_result = delete_expense(expense_id)

    flash(db_result['message'], db_result['result'])

    return redirect(back)