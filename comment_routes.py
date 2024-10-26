# comments.py
from flask import Blueprint, jsonify
from models import Comment
from auth_routes import login_required

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@login_required
def comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify([comment.to_dict() for comment in comments])
