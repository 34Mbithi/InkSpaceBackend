from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response, current_app
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from server.extensions import db
from server.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta

auth_ns = Namespace('auth', description='Authentication related operations')

class Register(Resource):
    def post(self):
        data = request.get_json()
        if not data or not all(key in data for key in ('username', 'email', 'password')):
            return make_response(jsonify({'message': 'Username, email, and password are required.'}), 400)

        username = data['username']
        email = data['email']
        password = data['password']

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            current_app.logger.warning("Attempted registration with existing username/email.")
            return make_response(jsonify({'message': 'Username or Email already exists'}), 400)

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            token = create_access_token(identity=new_user.id, expires_delta=timedelta(hours=1))
            current_app.logger.info(f"User {username} registered successfully with ID {new_user.id}")
            return make_response(jsonify({'message': 'User registered successfully', 'token': token}), 201)
        except IntegrityError:
            db.session.rollback()
            current_app.logger.error("Integrity error during user registration.")
            return make_response(jsonify({'message': 'Could not register user due to database error'}), 400)
        except Exception as e:
            current_app.logger.error(f"Unexpected error registering user: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)

class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return make_response(jsonify({'message': 'Email and password are required.'}), 400)

        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            current_app.logger.info(f"User {user.id} logged in successfully.")
            return make_response(jsonify({'message': 'Logged in successfully', 'token': token}), 200)
        else:
            current_app.logger.warning("Failed login attempt.")
            return make_response(jsonify({'message': 'Invalid email or password'}), 401)

class Logout(Resource):
    @jwt_required()
    def delete(self):
        
        current_user_id = get_jwt_identity()
        current_app.logger.info(f"User {current_user_id} logged out successfully.")
        
        return make_response(jsonify({"message": "Logged out successfully"}), 204)


class DeleteUser(Resource):
    @jwt_required()
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user:
            return {'message': 'User not found'}, 404

        user_to_delete = User.query.get(user_id)
        
        if not user_to_delete:
            return {'message': 'User not found'}, 404

        # Authorization check
        if user_to_delete.id != current_user.id and not current_user.is_admin:
            return {'message': 'Unauthorized action'}, 403

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        except SQLAlchemyError as e:
            current_app.logger.error(f"Error deleting user: {e}")
            return {'message': 'Failed to delete user, please try again later.'}, 500

# Add resources to the Namespace
auth_ns.add_resource(Register, '/register')
auth_ns.add_resource(Login, '/login')
auth_ns.add_resource(Logout, '/logout')
auth_ns.add_resource(DeleteUser, '/delete-user/<int:user_id>')
