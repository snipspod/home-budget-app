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

bp = Blueprint('user_account', __name__, url_prefix='/user')

@bp.route('/', methods=('GET',))
@login_required
def index():
    
    from home_budget_app.db import get_user_statistics

    stats = get_user_statistics(g.user['email'])
    
    return render_template('user_account.html', stats=stats)

@bp.route('/', methods=('POST',))
@login_required
def change_password():
    from home_budget_app.db import update_password
    back = request.referrer

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        update_msg = update_password(g.user['email'], old_password, new_password)

        print(update_msg)

        flash(update_msg['message'], update_msg['result'])
        return redirect(back)


