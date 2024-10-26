from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Text
from sqlalchemy.orm import relationship, validates
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for many-to-many relationship between BlogPost and Category
post_category = Table(
    'post_category',
    db.Model.metadata,
    Column('post_id', Integer, ForeignKey('blog_posts.id', ondelete="CASCADE"), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete="CASCADE"), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)  # Stores hashed password
    created_at = Column(DateTime, default=datetime.now)

    # Relationship to BlogPost
    posts = relationship('BlogPost', back_populates='author', cascade="all, delete")

    # Set password (hashed)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Validations for username and email
    @validates('username')
    def validate_username(self, key, username):
        assert username, "Username must not be empty"
        return username

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Provided email is invalid"
        return email

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),  # Convert datetime to ISO format
            'posts': [post.to_dict() for post in self.posts]  # Serialize related posts
        }

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    # Relationships
    author = relationship('User', back_populates='posts')
    categories = relationship('Category', secondary=post_category, back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade="all, delete")

    @validates('title')
    def validate_title(self, key, title):
        assert title, "Title must not be empty"
        return title

    @validates('content')
    def validate_content(self, key, content):
        assert content, "Content must not be empty"
        return content

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),  # Convert datetime to ISO format
            'author_id': self.author_id,
            'categories': [category.name for category in self.categories],  # Serialize categories
            'comments': [comment.to_dict() for comment in self.comments]  # Serialize comments
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Relationship to BlogPost
    posts = relationship('BlogPost', secondary=post_category, back_populates='categories')

    @validates('name')
    def validate_name(self, key, name):
        assert name, "Category name must not be empty"
        return name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'posts': [post.to_dict() for post in self.posts]  # Serialize related posts
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('blog_posts.id', ondelete="CASCADE"))

    # Relationship to BlogPost
    post = relationship('BlogPost', back_populates='comments')

    @validates('content')
    def validate_content(self, key, content):
        assert content, "Comment content must not be empty"
        return content

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),  # Convert datetime to ISO format
            'post_id': self.post_id
        }
