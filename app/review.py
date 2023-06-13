from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('review', __name__, url_prefix='/review')

@bp.route('/list')
@login_required
def list():
    return render_template('schedule/list.html')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        comment = request.form['comment']
        stars = request.form['stars']
        url_image = request.form['url_image']

        db, c = get_db()
        error = None

        if not comment or not stars:
            error = 'Please fill in all the fields'

        if error is None:
            c.execute(
                """
                INSERT INTO review
                ("comment", stars)
                VALUES(%s, %s)
                RETURNING id_review;
                """, (comment, stars)
            )
            review_row = c.fetchone()
            
            if review_row is not None:
                review_id = review_row['id_review']
                
                c.execute(
                    """
                    INSERT INTO review_user
                    (id_user, id_review)
                    VALUES(%s, %s);
                    """, (g.user['id_user'], review_id)
                )

                if url_image:
                    c.execute(
                        """
                        INSERT INTO image
                        (image_url, created_on, "type")
                        VALUES(%s, CURRENT_TIMESTAMP, 'review')
                        RETURNING id_image;
                        """,(url_image, )
                    )

                    image_row = c.fetchone()
                    if image_row is not None:
                        image_id = image_row['id_image']

                        c.execute(
                            """
                            INSERT INTO review_image
                            (id_review, id_image)
                            VALUES(%s, %s);
                            """, (review_id, image_id)
                        )
                    
                db.commit()
                
                return redirect(url_for('home.index'))

        flash(error)

    return render_template('review/create.html')
        