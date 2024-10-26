from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from .config import Config
from .extensions import db, bcrypt
from .routes.auth_routes import auth_ns
from .routes.comment_routes import comments_ns
from .routes.posts_routes import posts_ns
from .routes.profile_routes import profile_ns



migrate = Migrate()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    register_extensions(app)

    # Initialize Api and register namespaces
    api = Api(app)
    api.add_namespace(auth_ns, path='')
    api.add_namespace(comments_ns, path='')
    api.add_namespace(posts_ns, path='')
    api.add_namespace(profile_ns, path='')

    return app

def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db) 
