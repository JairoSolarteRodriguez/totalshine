from flask import (
    Blueprint, redirect, render_template, g, request, url_for, flash
)

from app.auth import admin_required
from app.db import get_db


bp = Blueprint('product', __name__, url_prefix='/admin/products')

@bp.route('/')
@admin_required
def list():
    db, c = get_db()

    c.execute("SELECT * FROM product p")

    products = c.fetchall()

    return render_template('admin/product/list.html', products=products)
        
@bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        url_image = request.form['url_image']
        price = request.form['price']
        active = request.form['active']

        db, c = get_db()
        error = None

        if not title or not price or not active:
            error = 'Please fill in all the fields'

        if error is None:
            
            c.execute(
                """
                    INSERT INTO public.product 
                    (title, description, url_image, price,active)
                    VALUES(%s, %s, %s, %s, %s);
                """, (title, description, url_image, price, active)
            )

            db.commit()

            return redirect(url_for('product.list'))

        flash(error)

    return render_template('admin/product/create.html')
        
@admin_required
def update():
    pass

@admin_required
def delete():
    pass