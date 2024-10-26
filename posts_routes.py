# posts.py
from flask import Blueprint, request, jsonify, make_response, session
from config import db
from models import BlogPost, Category
from auth_routes import login_required

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    if request.method == 'GET':
        posts = BlogPost.query.all()
        return jsonify([post.to_dict() for post in posts])

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

@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def get_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return jsonify(post.to_dict())
