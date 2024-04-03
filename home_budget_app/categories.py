from flask import Blueprint, flash, g, redirect, render_template, request

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

    category_id = request.form.get('category_id')

    db_result = delete_category(category_id)

    flash(db_result['message'], db_result['result'])
    return redirect(back)

@bp.route('/update', methods=('POST',))
@login_required
def update_category():
    from home_budget_app.db import update_category
    back = request.referrer

    category_id = request.form.get('category_id')
    category_new = request.form.get('category_new').strip()

    db_result = update_category(category_id, category_new)

    flash(db_result['message'], db_result['result'])
    return redirect(back)

@bp.route('/add', methods=('POST',))
@login_required
def add_category():
    back = request.referrer
    from home_budget_app.db import add_category

    category = request.form['category_name'].strip()

    db_result = add_category(g.user['email'], category)

    flash(db_result['message'], db_result['result'])
    return redirect(back)