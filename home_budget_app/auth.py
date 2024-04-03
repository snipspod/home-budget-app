import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from home_budget_app.db import create_user, get_user_by_email

bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        from home_budget_app.db import authenticate_user
        username = request.form.get('email')
        password = request.form.get('password')

        db_result = authenticate_user(username, password)

        if 'user' in db_result:
            session.clear()
            session.permanent = True
            session['user_email'] = db_result['user'].get('email')
            flash(db_result['message'], db_result['result'])
            return redirect(url_for('dashboard.index'))
        else:
            flash(db_result['message'], db_result['result'])
            

    if request.method == "GET":
        if g.user is not None:
            return redirect(url_for('dashboard.index'))

    return render_template("login.html")



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        name = request.form.get('name')

        db_result = create_user(name, email, password, password_confirm)
            
        flash(db_result['message'], db_result['result'])
        if db_result['result'] == 'success':
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.register'))

    if request.method == "GET":
        if g.user is not None:
            return redirect(url_for('dashboard.index'))

    return render_template('register.html')
    

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.before_app_request
def load_logged_in_user():
    user_email = session.get("user_email")
    if user_email is None:
        g.user = None
    else:
        g.user = get_user_by_email(user_email)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

