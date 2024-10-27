from flask_restx import Namespace, Resource
from flask import jsonify
from server.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

profile_ns = Namespace('profile', description='User profile operations')

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        if user:
            return user.to_dict(), 200
        else:
            return {'error': 'User not found'}, 404

profile_ns.add_resource(UserProfile, '')
