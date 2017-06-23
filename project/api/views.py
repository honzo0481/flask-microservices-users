"""User views module."""

from flask import Blueprint, jsonify

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    """You ping. I pong."""
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
