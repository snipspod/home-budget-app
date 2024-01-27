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

bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('/', methods=('GET',))
@login_required
def index():
    from home_budget_app.db import get_user_categories

    categories = get_user_categories(g.user['email'])

    return render_template('categories.html', categories=categories)

@bp.route('/delete', methods=('POST',))
@login_required
def delete_category():
    from home_budget_app.db import delete_category
    back = request.referrer

    category = request.form['category']

    db_result = delete_category(g.user['email'], category)

    flash(db_result['message'], db_result['result'])
    return redirect(back)

@bp.route('/update', methods=('POST',))
@login_required
def update_category():
    from home_budget_app.db import update_category
    back = request.referrer

    category_old = request.form['category_old']
    category_new = request.form['category_new']

    db_result = update_category(g.user['email'], category_old, category_new)

    flash(db_result['message'], db_result['result'])
    return redirect(back)
