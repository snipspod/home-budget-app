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
        from home_budget_app.db import get_user_expenses
        
        expenses = get_user_expenses(g.user['email'])

        return render_template('expenses/expenses_history.html', expenses=expenses)