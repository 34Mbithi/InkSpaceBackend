from flask import request, jsonify
from server.models import Comment, db
from flask_restx import Namespace, Resource

comments_ns = Namespace('comments', description='Comment-related operations')

class CommentList(Resource):
    def get(self, post_id):
        """Retrieve all comments for a specific post."""
        comments = Comment.query.filter_by(post_id=post_id).all()
        return jsonify([comment.to_dict() for comment in comments])

    def post(self, post_id):
        """Create a new comment for a specific post."""
        data = request.get_json()
        content = data.get("content")
        
        if not content:
            return {"message": "Content is required"}, 400
        
        new_comment = Comment(content=content, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        
        return new_comment.to_dict(), 201

class CommentItem(Resource):
    def get(self, post_id, comment_id):
        """Retrieve a specific comment."""
        comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first()
        if not comment:
            return {"message": "Comment not found"}, 404
        return comment.to_dict()

    def put(self, post_id, comment_id):
        """Update a specific comment."""
        comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first()
        if not comment:
            return {"message": "Comment not found"}, 404

        data = request.get_json()
        content = data.get("content")
        
        if not content:
            return {"message": "Content is required"}, 400

        comment.content = content
        db.session.commit()
        
        return comment.to_dict(), 200

    def delete(self, post_id, comment_id):
        """Delete a specific comment."""
        comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first()
        if not comment:
            return {"message": "Comment not found"}, 404

        db.session.delete(comment)
        db.session.commit()
        
        return {"message": "Comment deleted successfully"}, 200

# Register resources with paths in the namespace
comments_ns.add_resource(CommentList, '/posts/<int:post_id>/comments')
comments_ns.add_resource(CommentItem, '/posts/<int:post_id>/comments/<int:comment_id>')
