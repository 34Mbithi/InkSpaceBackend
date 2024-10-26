# posts.py
from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response, session
from server.extensions import db
from server.models import BlogPost, Category
from server.routes.auth_routes import login_required

posts_ns = Namespace('posts', description='Post related operations')

class PostList(Resource):
    @login_required
    def get(self):
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

class SinglePost(Resource):
    @login_required
    def get(self, post_id):
        post = BlogPost.query.get_or_404(post_id)
        return jsonify(post.to_dict())

# Add the resources to the Namespace
posts_ns.add_resource(PostList, '')
posts_ns.add_resource(SinglePost, '/<int:post_id>')
