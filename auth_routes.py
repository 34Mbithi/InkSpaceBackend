from flask import Blueprint, request, session, jsonify, make_response, current_app
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from config import db
from models import User
from functools import wraps
import logging

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return make_response(jsonify({'message': 'You need to log in first.'}), 401)
        return f(*args, **kwargs)
    return wrap

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, email, password = data.get('username'), data.get('email'), data.get('password')
    
    if User.query.filter_by(email=email).first():
        return make_response(jsonify({"message": "User already exists"}), 400)

    new_user = User(username=username, email=email)  
    new_user.password_hash = password  
    try:
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id  # Set session variable after user creation
        return make_response(jsonify({"message": "User created successfully", "token": "your_token_here"}), 201)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({'error': 'IntegrityError: Unable to process the entity'}), 422)

@auth_bp.route('/login', methods=['POST'])
def login():
    
    current_app.logger.info("Login route hit with request: %s", request.get_json())
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.authenticate(password):
        session['user_id'] = user.id
        return jsonify(user.to_dict()), 200
    
    return make_response(jsonify({"message": "Invalid email or password"}), 401)

@auth_bp.route('/logout', methods=['DELETE'])
@login_required
def logout():
    session.pop('user_id', None)
    return make_response(jsonify({"message": "Logged out successfully"}), 204)
