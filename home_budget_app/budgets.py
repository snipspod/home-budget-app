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

bp = Blueprint('budgets', __name__, url_prefix='/budgets')

@bp.route('/', methods=('GET',))
@login_required
def index():
    from home_budget_app.db import get_user_categories, get_user_budgets, get_historical_user_budgets

    categories = get_user_categories(g.user['email'])
    budgets = get_user_budgets(g.user['email'])
    historical_budgets = get_historical_user_budgets(g.user['email'])

    return render_template('budgets.html', categories=categories, budgets=budgets, historical_budgets=historical_budgets)

@bp.route('/add-budget', methods=('POST',))
@login_required
def add_budget():
    from home_budget_app.db import add_budget
    back = request.referrer
    name = request.form.get('budget_name')
    budget_amount = float(request.form.get('budget_amount').replace(',', '.'))
    budget_month = int(request.form.get('budget_month'))
    assoc_categories = []

    for key in request.form.keys():
        if 'include' in key:
            assoc_categories.append(
                {
                    'category_id': key.removeprefix('include_'),
                    'amount': float(request.form.get('budget_amount').replace(',', '.')) * float(request.form.get(f"percentage_{key.removeprefix('include_')}"))/100.0
                }
            )

    db_result = add_budget(g.user['email'], name, budget_amount, assoc_categories, budget_month)
    flash(db_result['message'], db_result['result'])
    return redirect(back)

@bp.route('/update-budget', methods=('POST',))
@login_required
def update_budget():
    from home_budget_app.db import update_budget
    back = request.referrer
    budget_name = request.form.get('new_budget_name')
    budget_amount = float(request.form.get('new_budget_amount').replace(',', '.'))
    budget_month = int(request.form.get('new_budget_month'))
    budget_id = request.form.get('budget_id')
    assoc_categories = []

    for key in request.form.keys():
        if 'include' in key:
            assoc_categories.append(
                {
                    'category_id': key.removeprefix('include_'),
                    'amount': budget_amount * float(request.form.get(f"percentage_{key.removeprefix('include_')}"))/100.0
                }
            )
        
    db_result = update_budget(budget_id, budget_month, budget_amount, budget_name, assoc_categories)
    flash(db_result['message'], db_result['result'])

    return redirect(back)

@bp.route('/delete-budget', methods=('POST',))
@login_required
def delete_budget():
    from home_budget_app.db import delete_budget
    back = request.referrer

    budget_id = request.form.get('budget_id')

    db_result = delete_budget(budget_id)
        
    flash(db_result['message'], db_result['result'])
    
    return redirect(back)