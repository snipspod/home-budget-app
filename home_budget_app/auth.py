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

        username = request.form['email']
        password = request.form['password']

        user = authenticate_user(username, password)

        if type(user) is not Exception:
            session.clear()
            session['user_email'] = user.get('email')
            return redirect(url_for('dashboard.index'))
        else:
            flash(user, 'warning')

    if request.method == "GET":
        if g.user is not None:
            return redirect(url_for('dashboard.index'))


    return render_template("auth/login.html")



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        error = None
        
        if error is None:
            try:
                create_user(name, email, password)
            except Exception as e:
                error = e
            else:
                flash("User successfully created!", 'success')
                return redirect(url_for('auth.login'))
        flash(error, 'warning')

    if request.method == "GET":
        if g.user is not None:
            return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')
    

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

