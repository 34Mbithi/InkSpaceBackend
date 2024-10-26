import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)  


load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='../client/build', template_folder='../client/build')
app.config['SECRET_KEY'] = os.getenv('SECTRET_KEY','f550003f7c3dc2211c5ef4ec3a1f50ce123e11ec4b40f23aeb5ebbd88c7672d3')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql://db_7ewv_user:v9Uz0sQWWlysSawYMBMq1nuQD6AffE7T@dpg-cseh2fm8ii6s7393u1m0-a/db_7ewv')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)
api = Api(app)

db.init_app(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')
