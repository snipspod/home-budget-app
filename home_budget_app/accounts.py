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
    return redirect(back)

@bp.route('/delete-account', methods=('POST',))
@login_required
def delete_account():
    back = request.referrer
    return redirect(back)