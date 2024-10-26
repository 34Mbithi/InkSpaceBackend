# Standard library imports
import datetime
from random import randint, choice as rc
# Remote library imports
from config import app, db
from models import User, BlogPost, Category, Comment
from faker import Faker

# Initialize Faker instance
fake = Faker()

# Function to seed the database
def seed_data():
    with app.app_context():
        print("Starting seed...")
        # Delete all rows in tables
        Comment.query.delete()
        BlogPost.query.delete()
        User.query.delete()
        Category.query.delete()
        db.session.commit()

        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # Add categories
        CATEGORIES = ["Technology", "Science", "Art", "Travel", "Health"]
        categories = [Category(name=category) for category in CATEGORIES]
        db.session.add_all(categories)
        db.session.commit()

        # Seed Users
        users = seed_users(num_users=10)  # Create 10 users
        # Seed Blog Posts
        posts = seed_blog_posts(users, categories, num_posts=20)  # Create 20 blog posts
        # Seed Comments
        seed_comments(users, posts, num_comments=50)  # Create 50 comments

        print("Database seeded successfully!")

def seed_users(num_users=5):
    users = []
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            _password_hash='password123'  # You can add password hashing here if needed
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
    return users

def seed_categories():
    categories = ['Technology', 'Lifestyle', 'Travel', 'Food', 'Education']
    category_objs = []
    for name in categories:
        category = Category(name=name)
        category_objs.append(category)
        db.session.add(category)
    db.session.commit()
    return category_objs

def seed_blog_posts(users, categories, num_posts=10):
    posts = []
    for _ in range(num_posts):
        post = BlogPost(
            title=fake.sentence(nb_words=6),
            content=fake.text(max_nb_chars=200),
            user_id=rc(users).id,
            created_at=datetime.datetime.utcnow()  # Corrected reference
        )
        # Assign random categories to the post
        categories_to_assign = set()
        while len(categories_to_assign) < randint(1, 5):
            category = rc(categories)
            categories_to_assign.add(category)
        
        post.categories = list(categories_to_assign)  # Assign categories to the post
        posts.append(post)
    db.session.add_all(posts)
    db.session.commit()
    return posts

def seed_comments(users, posts, num_comments=20):
    comments = []
    for _ in range(num_comments):
        comment = Comment(
            content=fake.sentence(nb_words=10),
            post_id=rc(posts).id,
            user_id=rc(users).id,
            created_at=datetime.datetime.utcnow()  # Corrected reference
        )
        comments.append(comment)
    db.session.add_all(comments)
    db.session.commit()

if __name__ == '__main__':
    seed_data()