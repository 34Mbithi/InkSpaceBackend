import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f550003f7c3dc2211c5ef4ec3a1f50ce123e11ec4b40f23aeb5ebbd88c7672d3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://inkspacedb_7lj9_user:T7vXgPHOqFt2RHhPODHruXhjpnd1l4iX@dpg-csekh8rtq21c738dnhbg-a.oregon-postgres.render.com/inkspacedb_7lj9'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT SETTINGS
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fb7735a66fa196e5ed0eb045e3f00f12e6722f88b1793840fb273c4b37dc1d5a') 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = False  # Disable in production; only for local testing
    JWT_COOKIE_CSRF_PROTECT = False  # Disable CSRF protection for testing purposes
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_HEADER_TYPE = 'Bearer'


    
