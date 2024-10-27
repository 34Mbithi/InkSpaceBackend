from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import timedelta
from .config import Config
from .extensions import db, bcrypt
from .routes.auth_routes import auth_ns
from .routes.comment_routes import comments_ns
from .routes.posts_routes import posts_ns
from .routes.profile_routes import profile_ns
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    
    # Set CORS to allow specific origin and credentials
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response

    jwt = JWTManager(app)
    jwt.init_app(app)    


    # Initialize extensions
    register_extensions(app)

    # Initialize Api and register namespaces
    api = Api(app)
    api.add_namespace(auth_ns, path='')
    api.add_namespace(comments_ns, path='')
    api.add_namespace(posts_ns, path='')
    api.add_namespace(profile_ns, path='/profile')

    return app

def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)