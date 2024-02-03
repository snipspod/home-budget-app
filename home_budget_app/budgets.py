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
    from home_budget_app.db import get_user_categories

    categories = get_user_categories(g.user['email'])

    return render_template('budgets.html', categories=categories)
