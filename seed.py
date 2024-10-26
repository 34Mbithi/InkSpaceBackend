from server import create_app
from server.extensions import db
from server.models import User, BlogPost, Category, Comment
from datetime import datetime

app = create_app()
with app.app_context():
    # Drop existing tables and create new ones
    db.drop_all()
    db.create_all()

    # Seed Users
    users = [
        User(username='alice', email='alice@example.com', password_hash='hashed_password_1'),
        User(username='bob', email='bob@example.com', password_hash='hashed_password_2'),
        User(username='charlie', email='charlie@example.com', password_hash='hashed_password_3'),
        User(username='dave', email='dave@example.com', password_hash='hashed_password_4'),
        User(username='eve', email='eve@example.com', password_hash='hashed_password_5'),
    ]
    
    db.session.bulk_save_objects(users)
    db.session.commit()

    # Seed Categories
    categories = [
        Category(name='Technology'),
        Category(name='Health'),
        Category(name='Travel'),
        Category(name='Education'),
        Category(name='Lifestyle'),
    ]
    
    db.session.bulk_save_objects(categories)
    db.session.commit()

    # Seed Blog Posts
    posts = [
        BlogPost(title='The Future of Tech', content='Discussion about AI and ML.', author_id=1, created_at=datetime.utcnow()),
        BlogPost(title='Healthy Living Tips', content='Tips on maintaining a healthy lifestyle.', author_id=2, created_at=datetime.utcnow()),
        BlogPost(title='Top 10 Travel Destinations', content='A guide to the best places to visit.', author_id=3, created_at=datetime.utcnow()),
        BlogPost(title='Learning Python', content='A beginner\'s guide to programming.', author_id=4, created_at=datetime.utcnow()),
        BlogPost(title='Work-Life Balance', content='How to achieve balance in life.', author_id=5, created_at=datetime.utcnow()),
    ]
    
    db.session.bulk_save_objects(posts)
    db.session.commit()

    # Seed Comments
    comments = [
        Comment(content='Great insights!', post_id=1),
        Comment(content='Very informative, thank you!', post_id=2),
        Comment(content='Loved the suggestions!', post_id=3),
        Comment(content='Looking forward to applying these tips.', post_id=4),
        Comment(content='This helped me a lot, thanks!', post_id=5),
    ]
    
    db.session.bulk_save_objects(comments)
    db.session.commit()

    print("Database seeded!")
