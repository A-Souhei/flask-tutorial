from flask import render_template
from app import db
from app.errors import bp # this is the blueprint


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Important to rollback the session in case of error
    return render_template('errors/500.html'), 500
