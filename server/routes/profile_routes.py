# profile.py
from flask_restx import Namespace, Resource
from flask import jsonify, make_response, session
from server.models import User
from server.routes.auth_routes import login_required

profile_ns = Namespace('profile', description='User profile operations')

class UserProfile(Resource):
    @login_required
    def get(self):
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        return make_response(jsonify(user.to_dict()), 200) if user else {'error': 'User not found'}, 404

# Add the resource to the Namespace
profile_ns.add_resource(UserProfile, '/profile')
