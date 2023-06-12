from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('schedule', __name__)

@bp.route('/')
# @login_required
def index():
    db, c = get_db()
    c.execute(
        """
            SELECT s.id_schedule, ua.id_user, concat(ua."name",' ', ua.last_name) AS "full name", ua.phone_number, ua.email,
            s.scheduling_date, s.schedule_for, s.address, s.phone AS "schedule phone", s.notes, s.schedule_state
            FROM schedule s
            INNER JOIN user_app ua ON s.id_user = ua.id_user;
        """
    )

    schedules = c.fetchall()

    return render_template('schedule/index.html', schedules=schedules)

@bp.route('/create')
@login_required
def create():
    pass