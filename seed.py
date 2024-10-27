from datetime import datetime
from server import create_app
from server.extensions import db
from server.models import User, BlogPost, Category, Comment

app = create_app()

# Ensure to run in app context
with app.app_context():
    # Drop all existing data and recreate tables
    db.drop_all()
    db.create_all()

    # Create sample users
    user1 = User(username='user1', email='user1@example.com')
    user1.set_password('password1')
    user2 = User(username='user2', email='user2@example.com')
    user2.set_password('password2')
    db.session.add_all([user1, user2])

    # Create sample categories
    category1 = Category(name="Technology")
    category2 = Category(name="Science")
    db.session.add_all([category1, category2])

    # Create sample blog posts
    post1 = BlogPost(title="First Post", content="Content of the first post.", author=user1)
    post1.categories.append(category1)
    post2 = BlogPost(title="Second Post", content="Content of the second post.", author=user2)
    post2.categories.append(category2)
    db.session.add_all([post1, post2])

    # Create sample comments
    comment1 = Comment(content="This is a comment on the first post.", post=post1)
    comment2 = Comment(content="Another comment on the first post.", post=post1)
    comment3 = Comment(content="This is a comment on the second post.", post=post2)
    db.session.add_all([comment1, comment2, comment3])

    # Commit all changes to the database
    db.session.commit()
    print("Database seeded successfully!")
