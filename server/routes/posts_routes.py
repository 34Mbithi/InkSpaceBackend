from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.extensions import db
from server.models import BlogPost, Category

posts_ns = Namespace('posts', description='Post related operations')

class PostList(Resource):
    @jwt_required()  # Require a valid JWT to access the post retrieval and creation routes
    def get(self):
        """Fetch all blog posts."""
        posts = BlogPost.query.all()
        current_app.logger.info("Fetched all blog posts.")
        return jsonify([post.to_dict() for post in posts])

    @jwt_required()
    def post(self):
        """Create a new blog post."""
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        category_names = data.get('categories', [])

        user_id = get_jwt_identity()  # Retrieve user ID from JWT token
        current_app.logger.info(f"User {user_id} is attempting to create a post.")

        post = BlogPost(
            title=title,
            content=content,
            author_id=user_id
        )

        for name in category_names:
            category = Category.query.filter_by(name=name).first()
            if not category:
                category = Category(name=name)
                db.session.add(category)
            post.categories.append(category)

        db.session.add(post)
        db.session.commit()

        current_app.logger.info(f"Post created by user_id: {user_id} with post_id: {post.id}")
        return make_response(jsonify(post.to_dict()), 201)

class SinglePost(Resource):
    @jwt_required()  # Require a valid JWT for accessing single posts
    def get(self, post_id):
        """Fetch a single blog post by ID."""
        post = BlogPost.query.get_or_404(post_id)
        current_app.logger.info(f"Fetched post with ID {post_id}")
        return jsonify(post.to_dict())

    @jwt_required()
    def put(self, post_id):
        """Update an existing blog post."""
        data = request.get_json()
        post = BlogPost.query.get_or_404(post_id)

        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)

        # Optionally handle categories
        category_names = data.get('categories', [])
        post.categories.clear()  # Clear existing categories

        for name in category_names:
            category = Category.query.filter_by(name=name).first()
            if not category:
                category = Category(name=name)
                db.session.add(category)
            post.categories.append(category)

        db.session.commit()
        current_app.logger.info(f"Post updated with ID {post_id}")
        return jsonify(post.to_dict())

    @jwt_required()
    def delete(self, post_id):
        """Delete a blog post by ID."""
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        current_app.logger.info(f"Post deleted with ID {post_id}")
        return make_response(jsonify({"message": "Post deleted"}), 204)

# Add resources to the Namespace
posts_ns.add_resource(PostList, '')
posts_ns.add_resource(SinglePost, '/<int:post_id>')
