# comments.py
from flask_restx import Namespace, Resource
from flask import jsonify
from server.models import Comment
from server.routes.auth_routes import login_required

comments_ns = Namespace('comments', description='Comment related operations')

class CommentList(Resource):
    @login_required
    def get(self, post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        return jsonify([comment.to_dict() for comment in comments])

# Add the resource to the Namespace
comments_ns.add_resource(CommentList, '/posts/<int:post_id>/comments')
