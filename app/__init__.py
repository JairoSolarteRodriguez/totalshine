import os
from flask import Flask, g

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY = 'totalshine',
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE_PORT = os.environ.get('FLASK_DATABASE_PORT'),
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE = os.environ.get('FLASK_DATABASE'),
    )

    from . import db
    
    db.init_app(app)

    from . import auth, schedule, home, review

    from .admin import admin, product, hire, review_admin

    app.register_blueprint(auth.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(review.bp)

    # Register bp admin
    app.register_blueprint(admin.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(hire.bp)
    app.register_blueprint(review_admin.bp)

    return app