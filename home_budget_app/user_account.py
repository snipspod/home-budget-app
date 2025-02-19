from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from home_budget_app.auth import login_required

bp = Blueprint('user_account', __name__, url_prefix='/user')

@bp.route('/', methods=('GET',))
@login_required
def index():
    
    from home_budget_app.db import get_user_statistics

    stats = get_user_statistics(g.user['email'])
    print(stats)
    
    return render_template('user_account.html', stats=stats)

@bp.route('/change-passwordchange-password', methods=('POST',))
@login_required
def change_password():
    from home_budget_app.db import update_password
    back = request.referrer

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        update_msg = update_password(g.user['email'], old_password, new_password)

        flash(update_msg['message'], update_msg['result'])
        return redirect(back)
    

@bp.route('/delete-account', methods=('POST',))
@login_required
def delete_account():
    from home_budget_app.db import delete_user_account

    back = request.referrer
    password = request.form.get('password')

    db_result = delete_user_account(g.user['email'], password)

    if db_result['result'] == 'success':
        session.clear()
        flash(db_result['message'], db_result['result'])
        return redirect(url_for('auth.login'))
    else:
        flash(db_result['message'], db_result['result'])
        return redirect(back)



