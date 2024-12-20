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
        if not username or username.strip() == "":
            raise ValueError("Username must not be empty")
        return username

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Provided email is invalid")
        return email

    def to_dict(self, include_posts=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),  # Convert datetime to ISO format
        }
        if include_posts:
            data['posts'] = [post.to_dict() for post in self.posts]  # Serialize related posts
        return data

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

    def to_dict(self, include_author=True, include_categories=True, include_comments=False):
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),  # Convert datetime to ISO format
            'author_id': self.author_id,
        }
        if include_author and self.author:
            data['author'] = {
                'id': self.author.id,
                'username': self.author.username,
            }
        if include_categories:
            data['categories'] = [category.to_dict() for category in self.categories]
        if include_comments:
            data['comments'] = [comment.to_dict() for comment in self.comments]
        return data


class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Relationship to BlogPost
    posts = relationship('BlogPost', secondary=post_category, back_populates='categories')

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Category name must not be empty")
        return name

    def to_dict(self, include_posts=False):
        data = {
            'id': self.id,
            'name': self.name,
        }
        if include_posts:
            data['posts'] = [post.to_dict() for post in self.posts] 
        return data

class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('blog_posts.id', ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    # Relationships
    post = relationship('BlogPost', back_populates='comments')
    author = relationship('User')  # Add a relationship to User if desired

    @validates('content')
    def validate_content(self, key, content):
        if not content or content.strip() == "":
            raise ValueError("Comment content must not be empty")
        return content

    def to_dict(self, include_post=False, include_author=False):
        data = {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'post_id': self.post_id,
            'author_id': self.author_id,  # Include author_id if needed
            'author':{"username":self.author.username} if self.author else None
        }
        if include_post:
            data['post'] = self.post.to_dict()
        if include_author and self.author:
            data['author'] = self.author.to_dict()
        return data
