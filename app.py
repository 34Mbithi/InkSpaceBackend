#!/usr/bin/env python3

from datetime import datetime
from functools import wraps
from flask import make_response, request, session, jsonify, abort
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models import User, BlogPost, Category, Comment

app.config['SECRET_KEY'] = 'f550003f7c3dc2211c5ef4ec3a1f50ce123e11ec4b40f23aeb5ebbd88c7672d3'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return make_response(jsonify({'message': 'You need to log in first.'}), 401)
        return f(*args, **kwargs)
    return wrap

class Register(Resource):
    def post(self):
        data = request.get_json()
        username, email, password = data.get('username'), data.get('email'), data.get('password')
        
        if User.query.filter_by(email=email).first():
            return make_response(jsonify({"message": "User already exists"}), 400)

        new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return make_response(jsonify({"message": "User created successfully", "token": "your_token_here"}), 201)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'IntegrityError: Unable to process the entity'}), 422)

class Login(Resource):
    def post(self):
        data = request.get_json()
        email, password = data.get('email'), data.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return make_response(jsonify({"message": "Invalid email or password"}), 401)

class ProfileResource(Resource):
    @login_required
    def get(self):
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        return make_response(jsonify(user.to_dict()), 200) if user else {'error': 'User not found'}, 404

class Logout(Resource):
    @login_required
    def delete(self):
        session.pop('user_id', None)
        return make_response(jsonify({"message": "Logged out successfully"}), 204)

class BlogPostResource(Resource):
    @login_required
    def get(self, post_id=None):
        if post_id:
            post = BlogPost.query.get_or_404(post_id)
            return jsonify(post.to_dict())
        posts = BlogPost.query.all()
        return jsonify([post.to_dict() for post in posts])

    @login_required
    def post(self):
        data = request.get_json()
        title, content, category_names = data.get('title'), data.get('content'), data.get('categories', [])
        
        user_id = session['user_id']
        post = BlogPost(title=title, content=content, author_id=user_id)
        
        for name in category_names:
            category = Category.query.filter_by(name=name).first() or Category(name=name)
            db.session.add(category)
            post.categories.append(category)

        db.session.add(post)
        db.session.commit()
        return make_response(jsonify(post.to_dict()), 201)

class CommentResource(Resource):
    @login_required
    def get(self, post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        return jsonify([comment.to_dict() for comment in comments])

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(ProfileResource, '/profile')
api.add_resource(BlogPostResource, '/posts', '/posts/<int:post_id>')
api.add_resource(CommentResource, '/posts/<int:post_id>/comments')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
