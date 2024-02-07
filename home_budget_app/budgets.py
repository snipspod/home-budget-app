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
    from home_budget_app.db import get_user_categories, get_user_budgets

    categories = get_user_categories(g.user['email'])
    budgets = get_user_budgets(g.user['email'])

    print(budgets)
    return render_template('budgets.html', categories=categories, budgets=budgets)

@bp.route('/add-budget', methods=('POST',))
@login_required
def add_budget():
    from home_budget_app.db import add_budget
    back = request.referrer
    name = request.form.get('budget_name')
    budget_amount = float(request.form.get('budget_amount').replace(',', '.'))
    assoc_categories = []

    print(request.form)

    for key in request.form.keys():
        if 'include' in key:
            assoc_categories.append(
                {
                    'category_id': key.removeprefix('include_'),
                    'amount': float(request.form.get('budget_amount').replace(',', '.')) * float(request.form.get(f'percentage_{key.removeprefix('include_')}'))/100.0
                }
            )

    db_result = add_budget(g.user['email'], name, budget_amount, assoc_categories)
    flash(db_result['message'], db_result['result'])
    return redirect(back)