from config import db, app
from models import User, BlogPost, Category, Comment
from werkzeug.security import generate_password_hash

def seed_data():
    # Create multiple users
    users = [
        User(username='john_doe', email='john@example.com'),
        User(username='jane_smith', email='jane@example.com'),
        User(username='alice_jones', email='alice@example.com'),
        User(username='bob_brown', email='bob@example.com'),
    ]

    # Set passwords using the property setter
    users[0].password = 'password123'
    users[1].password = 'password456'
    users[2].password = 'password789'
    users[3].password = 'securepass'

    db.session.bulk_save_objects(users)  # Use bulk_save_objects for efficiency

    # Commit users to the database
    db.session.commit()

    # Create multiple categories
    categories = [
        Category(name='Technology'),
        Category(name='Lifestyle'),
        Category(name='Health'),
        Category(name='Travel'),
        Category(name='Food'),
    ]

    db.session.bulk_save_objects(categories)  # Bulk save for categories

    # Commit categories to the database
    db.session.commit()

    # Create multiple blog posts
    posts = [
        BlogPost(title='Latest Trends in Technology', content='Content about tech trends...', user_id=1),
        BlogPost(title='Healthy Living Tips', content='Content about health tips...', user_id=2),
        BlogPost(title='Traveling the World on a Budget', content='Content about budget travel...', user_id=3),
        BlogPost(title='Delicious Vegan Recipes', content='Content about vegan food...', user_id=4),
        BlogPost(title='Work-Life Balance', content='Content about balancing work and life...', user_id=1),
    ]

    db.session.bulk_save_objects(posts)  # Bulk save for posts

    # Commit posts to the database
    db.session.commit()

    # Assign categories to posts
    posts[0].categories.append(categories[0])  # Technology post
    posts[1].categories.append(categories[2])  # Health post
    posts[2].categories.append(categories[3])  # Travel post
    posts[3].categories.append(categories[4])  # Food post
    posts[4].categories.append(categories[1])  # Lifestyle post

    # Commit category assignments
    db.session.commit()

    # Create multiple comments
    comments = [
        Comment(content='Great post! Very informative.', user_id=2, post_id=1),
        Comment(content='Thanks for the tips!', user_id=1, post_id=2),
        Comment(content='I loved the vegan recipes!', user_id=3, post_id=4),
        Comment(content='Traveling on a budget is crucial!', user_id=4, post_id=3),
        Comment(content='Work-life balance is so important!', user_id=1, post_id=5),
    ]

    db.session.bulk_save_objects(comments)  # Bulk save for comments

    # Commit comments to the database
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_data()
