from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@bp.route('/list')
@login_required
def list():
    db, c = get_db()
    c.execute(
        """
            SELECT s.id_schedule, ua.id_user, concat(ua."name",' ', ua.last_name) AS "full name", ua.phone_number, ua.email,
            s.scheduling_date, s.schedule_for, s.address, s.phone AS "schedule phone", s.notes, s.schedule_state
            FROM schedule s
            INNER JOIN user_app ua ON s.id_user = ua.id_user WHERE ua.id_user = %s ORDER BY s.scheduling_date DESC LIMIT 5;
        """,(g.user['id_user'],)
    )

    schedules = c.fetchall()

    return render_template('schedule/list.html', schedules=schedules)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        user_id = g.user['id_user']
        schedule_for = request.form['date_for']
        address = request.form['address']
        phone = request.form['phone']
        notes = request.form['notes']
        email = request.form['email']

        # conection
        db, c = get_db()
        error = None
        message = None

        if not schedule_for or not address or not notes or not email:
            error = 'please fill in all the fields'

        if error is None:
            c.execute(
                """
                    INSERT INTO public.schedule
                    (id_user, schedule_for, address, phone, notes, email)
                    VALUES(%s, %s, %s, %s, %s, %s);
                """, (user_id, schedule_for, address, phone, notes, email)
            )
            db.commit()

            message = 'Your appointment has been successfully scheduled, in a few moments we will contact you.'
            flash(message=message)
            
            return redirect(url_for('schedule.list'))

        flash(error)
        
    return render_template('schedule/create.html')

@bp.route('/status')
@login_required
def status():
    return render_template('schedule/status.html')