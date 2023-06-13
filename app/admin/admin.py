from flask import (
    Blueprint, render_template, g
)

from app.auth import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@admin_required
def index():
    print(g.user['rol'])
    return render_template('admin/index.html')