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
from home_budget_app.db import create_user

bp = Blueprint("auth", __name__, url_prefix='/auth')

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        error = None

        flash(error)

    return render_template("auth/login.html")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        error = None    
        if not email:
            error = 'Email is required!'
        elif not password:
            error = 'Password is required!'
        elif not name:
            error = 'Name is required!'
        
        if error is None:
            try:
                create_user(name, email, password)
            except Exception as e:
                error = e
            else:
                return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')