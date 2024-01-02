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
from pymongo.errors import DuplicateKeyError
from home_budget_app.db import create_user, get_user
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        error = None

        try:
            get_user(username, password)
        except Exception as e:
            error = e
        else:
            return redirect(url_for('auth.login'))

        flash(error, 'warning')

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
            except DuplicateKeyError:
                error = f"User {email} already exist!"
            else:
                flash("User successfully created!", 'success')
                return redirect(url_for('auth.login'))
        flash(error, 'warning')

    return render_template('auth/register.html')