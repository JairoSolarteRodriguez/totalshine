import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']

        # Validate user
        db, c = get_db()
        error = None

        c.execute(
            'SELECT id_user from user_app where email = %s', (email,)
        )
        
        if not email:
            error = 'email is required'
        if not password:
            error = 'password is required'
        if not name:
            error = 'name is required'
        if not last_name:
            error = 'last name is required'
        elif c.fetchone() is not None:
            error = 'email {} is already registered'.format(email)

        if error is None:
            c.execute(
                """
                    INSERT INTO public.user_app
                    ("name", last_name, email, phone_number, "password")
                    VALUES(%s, %s, %s, %s, %s);
                """,(name, last_name, email, phone_number, generate_password_hash(password=password))
            )
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db, c = get_db()
        error = None

        c.execute('SELECT * FROM user_app WHERE email = %s', (email,))
        user = c.fetchone()

        if user is None:
            error = 'invalid username and/or password'
        elif not check_password_hash(user['password'], password=password):
            error = 'invalid username and/or password'

        if error is None:
            session.clear()
            session['user_id'] = user['id_user']

            return redirect(url_for('schedule.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'SELECT id_user, name, last_name, email, phone_number FROM user_app WHERE id_user = %s' ,(user_id, )
        )
        g.user = c.fetchone()
            
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('schedule.index'))
