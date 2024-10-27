# seed.py
from datetime import datetime
from werkzeug.security import generate_password_hash
from server import create_app
from server.extensions import db
from server.models import User, BlogPost, Category, Comment

app = create_app()

def seed_data():
    with app.app_context():
        # Drop and recreate tables
        db.drop_all()
        db.create_all()

        # Seed Users
        users = [
            User(username="john_doe", email="john@example.com", password_hash=generate_password_hash("password1")),
            User(username="jane_smith", email="jane@example.com", password_hash=generate_password_hash("password2")),
            User(username="michael_lee", email="michael@example.com", password_hash=generate_password_hash("password3"))
        ]
        db.session.add_all(users)
        db.session.commit()

        # Seed Categories
        categories = [
            Category(name="Technology"),
            Category(name="Lifestyle"),
            Category(name="Education")
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Seed BlogPosts
        blog_posts = [
            BlogPost(title="The Future of AI", content="Exploring the impact of AI on society.", author_id=users[0].id, created_at=datetime.now()),
            BlogPost(title="Healthy Living Tips", content="How to maintain a balanced lifestyle.", author_id=users[1].id, created_at=datetime.now()),
            BlogPost(title="Learning Python", content="An introduction to Python programming.", author_id=users[2].id, created_at=datetime.now())
        ]
        db.session.add_all(blog_posts)
        db.session.commit()

        # Link Categories to BlogPosts
        blog_posts[0].categories.append(categories[0])  # AI -> Technology
        blog_posts[1].categories.append(categories[1])  # Healthy Living -> Lifestyle
        blog_posts[2].categories.append(categories[2])  # Python -> Education
        db.session.commit()

        # Seed Comments
        comments = [
            Comment(content="Great article on AI!", post_id=blog_posts[0].id, created_at=datetime.now()),
            Comment(content="Thanks for the tips!", post_id=blog_posts[1].id, created_at=datetime.now()),
            Comment(content="Very helpful post on Python.", post_id=blog_posts[2].id, created_at=datetime.now())
        ]
        db.session.add_all(comments)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
