from flask import (
    Blueprint, redirect, render_template, g, request, url_for, flash
)

from app.auth import admin_required
from app.db import get_db


bp = Blueprint('hire', __name__, url_prefix='/admin/hire')

@bp.route('/')
@admin_required
def list():
    db, c = get_db()

    c.execute("SELECT * FROM hire h")

    hiring = c.fetchall()

    return render_template('admin/hire/list.html', hiring=hiring)
        
@bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        url_image = request.form['url_image']

        db, c = get_db()
        error = None

        if not title or not description:
            error = 'Please fill in all the fields'

        if error is None:
            
            c.execute(
                """
                    INSERT INTO public.hire
                    (title, description, url_image)
                    VALUES(%s, %s, %s);
                """, (title, description, url_image)
            )

            db.commit()

            return redirect(url_for('hire.list'))

        flash(error)

    return render_template('admin/hire/create.html')
        

def update():
    pass

def delete():
    pass