# auth.py
from flask_restx import Namespace, Resource
from flask import request, session, jsonify, make_response, current_app
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from server.extensions import db
from server.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
import jwt
import datetime


auth_ns = Namespace('auth', description='Authentication related operations')


def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def login_required(f):
    from functools import wraps

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return make_response(jsonify({'message': 'You need to log in first.'}), 401)
        return f(*args, **kwargs)
    return wrap

class Register(Resource):
    def post(self):
        data = request.get_json()

        # Validate incoming data
        if not data or not all(key in data for key in ('username', 'email', 'password')):
            return make_response(jsonify({'message': 'Username, email, and password are required.'}), 400)

        username = data['username']
        email = data['email']
        password = data['password']

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return make_response(jsonify({'message': 'Username already exists'}), 400)

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            return make_response(jsonify({'message': 'Email already exists'}), 400)

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)  # Hash the password
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'message': 'User registered successfully'}), 201)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'message': 'Could not register user due to database error'}), 400)
        except Exception as e:
            current_app.logger.error(f"Error registering user: {e}")
            return make_response(jsonify({'message': 'Internal server error'}), 500)
        

class Login(Resource):
    def post(self):
        current_app.logger.info("Login route hit with request: %s", request.get_json())
        data = request.get_json()

        # Validate incoming data
        if not data or not data.get('email') or not data.get('password'):
            return make_response(jsonify({'message': 'Email and password are required.'}), 400)

        email, password = data['email'], data['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password): 
            
            token = generate_jwt_token(user)  

            return make_response(jsonify({'message': 'Login successful', 'token': token}), 200)
        else:
            return make_response(jsonify({'message': 'Invalid email or password'}), 401)


class Logout(Resource):
    @login_required
    def delete(self):
        session.pop('user_id', None)
        return make_response(jsonify({"message": "Logged out successfully"}), 204)

class DeleteUser(Resource):
    @jwt_required()
    def delete(self, user_id):
        current_user_public_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_public_id).first()

        if not current_user:
            return {'message': 'User not found'}, 404

        user_to_delete = User.query.get(user_id)
        
        if not user_to_delete:
            return {'message': 'User not found'}, 404

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
