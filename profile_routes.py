# profile.py
from flask import Blueprint, jsonify, make_response, session
from models import User
from auth_routes import login_required

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return make_response(jsonify(user.to_dict()), 200) if user else {'error': 'User not found'}, 404
