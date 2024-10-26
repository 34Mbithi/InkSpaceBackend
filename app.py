# app.py
from config import app
from auth_routes import auth_bp
from profile_routes import profile_bp
from posts_routes import posts_bp
from comment_routes import comments_bp

app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
