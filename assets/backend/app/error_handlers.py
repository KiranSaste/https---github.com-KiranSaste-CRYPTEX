from flask import jsonify, render_template, Blueprint, current_app, request
from app import db

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api'):
        return jsonify({"error": "Resource not found"}), 404
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    # Log the error
    current_app.logger.error(error)
    db.session.rollback()
    if request.path.startswith('/api'):
        return jsonify({"error": "Internal server error"}), 500
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(403)
def forbidden_error(error):
    if request.path.startswith('/api'):
        return jsonify({"error": "Forbidden"}), 403
    return render_template('errors/403.html'), 403 