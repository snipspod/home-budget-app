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
    
    return render_template('user_account/user_account.html', stats=stats)