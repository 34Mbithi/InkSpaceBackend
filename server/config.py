# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f550003f7c3dc2211c5ef4ec3a1f50ce123e11ec4b40f23aeb5ebbd88c7672d3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://inkspacedb_7lj9_user:T7vXgPHOqFt2RHhPODHruXhjpnd1l4iX@dpg-csekh8rtq21c738dnhbg-a.oregon-postgres.render.com/inkspacedb_7lj9'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
