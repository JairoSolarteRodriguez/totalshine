from flask import (
    Blueprint, redirect, render_template, g, request, url_for, flash
)

from app.auth import admin_required
from app.db import get_db


bp = Blueprint('review_admin', __name__, url_prefix='/admin/review')

@bp.route('/')
@admin_required
def list():
    db, c = get_db()

    c.execute(
        """
            SELECT ua.id_user, ua."name", r.id_review, r."comment", r.stars, i.image_url  
            FROM review_user ru
            INNER JOIN user_app ua ON ru.id_user = ua.id_user
            INNER JOIN review r ON ru.id_review = r.id_review
            LEFT JOIN review_image ri on ri.id_review = r.id_review
            LEFT JOIN image i on i.id_image = ri.id_image 
        """
    )

    reviews = c.fetchall()

    return render_template('admin/review/list.html', reviews=reviews)
        

def update():
    pass

def delete():
    pass