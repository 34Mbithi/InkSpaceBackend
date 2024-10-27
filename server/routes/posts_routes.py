from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.extensions import db
from server.models import BlogPost, Category

posts_ns = Namespace('posts', description='Post related operations')

class PostList(Resource):
    def get(self):
        """Fetch all blog posts with optional pagination."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        current_app.logger.info(f"Fetching posts - page {page}, {per_page} per page.")
        
        posts = BlogPost.query.paginate(page=page, per_page=per_page, error_out=False)
        current_app.logger.info(f"Fetched {len(posts.items)} posts on page {page}.")
        
        return jsonify([post.to_dict(include_author=True, include_categories=True) for post in posts.items])

    @jwt_required()
    def post(self):
        """Create a new blog post."""
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        category_names = data.get('categories', [])

        user_id = get_jwt_identity()
        current_app.logger.info(f"User {user_id} is creating a post.")

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

        current_app.logger.info(f"Post created by user {user_id} with ID {post.id}")
        return make_response(jsonify(post.to_dict(include_author=True, include_categories=True)), 201)

class SinglePost(Resource):
    def get(self, post_id):
        """Fetch a single blog post by ID."""
        post = BlogPost.query.get_or_404(post_id)
        current_app.logger.info(f"Fetched post with ID {post_id}")
        return jsonify(post.to_dict(include_author=True, include_categories=True))

    @jwt_required()
    def put(self, post_id):
        """Update an existing blog post."""
        user_id = get_jwt_identity()
        post = BlogPost.query.get_or_404(post_id)

        if post.author_id != user_id:
            current_app.logger.warning(f"User {user_id} attempted to update post {post_id} without permission.")
            return make_response(jsonify({"message": "Permission denied"}), 403)

        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)

        # Handle categories
        category_names = data.get('categories', [])
        post.categories.clear()

        for name in category_names:
            category = Category.query.filter_by(name=name).first()
            if not category:
                category = Category(name=name)
                db.session.add(category)
            post.categories.append(category)

        db.session.commit()
        current_app.logger.info(f"Post {post_id} updated by user {user_id}")
        return jsonify(post.to_dict(include_author=True, include_categories=True))

    @jwt_required()
    def delete(self, post_id):
        """Delete a blog post by ID."""
        user_id = get_jwt_identity()
        post = BlogPost.query.get_or_404(post_id)

        if post.author_id != user_id:
            current_app.logger.warning(f"User {user_id} attempted to delete post {post_id} without permission.")
            return make_response(jsonify({"message": "Permission denied"}), 403)

        db.session.delete(post)
        db.session.commit()
        current_app.logger.info(f"Post {post_id} deleted by user {user_id}")
        return make_response(jsonify({"message": "Post deleted"}), 204)

# Add resources to the Namespace
posts_ns.add_resource(PostList, '')
posts_ns.add_resource(SinglePost, '/<int:post_id>')
