from datetime import datetime
from server import create_app
from server.extensions import db
from server.models import User, BlogPost, Category, Comment

app = create_app()

with app.app_context():
    # Drop all existing data and recreate tables
    db.drop_all()
    db.create_all()

    # Create sample users
    users = [
        User(username='alice', email='alice@example.com'),
        User(username='bob', email='bob@example.com'),
        User(username='carol', email='carol@example.com'),
        User(username='dave', email='dave@example.com'),
        User(username='eve', email='eve@example.com')
    ]
    for user in users:
        user.set_password('securepassword')  # Set same password for simplicity

    db.session.add_all(users)

    # Create sample categories
    categories = [
        Category(name="Technology"),
        Category(name="Science"),
        Category(name="Travel"),
        Category(name="Food"),
        Category(name="Lifestyle")
    ]
    db.session.add_all(categories)

    # Create sample blog posts and associate with users and categories
    blog_posts = [
        BlogPost(title="Exploring Quantum Computing", content="An in-depth look at quantum computing.", author=users[0]),
        BlogPost(title="Top 10 Travel Destinations", content="The best places to visit this year.", author=users[1]),
        BlogPost(title="The Future of AI", content="How AI will change the world.", author=users[2]),
        BlogPost(title="Healthy Recipes for a Balanced Diet", content="Delicious recipes that are good for you.", author=users[3]),
        BlogPost(title="Lifestyle Hacks for 2024", content="Simple lifestyle tips to improve your day.", author=users[4])
    ]

    # Assign categories to blog posts
    blog_posts[0].categories.extend([categories[0], categories[1]])
    blog_posts[1].categories.append(categories[2])
    blog_posts[2].categories.append(categories[0])
    blog_posts[3].categories.append(categories[3])
    blog_posts[4].categories.append(categories[4])

    db.session.add_all(blog_posts)

    # Create sample comments and associate them with blog posts and users
    comments = [
        Comment(content="Great insights on quantum computing!", post=blog_posts[0], author=users[1]),
        Comment(content="Can't wait to visit these places!", post=blog_posts[1], author=users[2]),
        Comment(content="AI is definitely going to shape our future.", post=blog_posts[2], author=users[3]),
        Comment(content="I love these recipes!", post=blog_posts[3], author=users[4]),
        Comment(content="Thanks for the tips!", post=blog_posts[4], author=users[0]),
        Comment(content="Really interesting read on AI.", post=blog_posts[2], author=users[4]),
        Comment(content="Adding this to my travel list!", post=blog_posts[1], author=users[3]),
        Comment(content="Looking forward to more posts on technology.", post=blog_posts[0], author=users[2])
    ]

    db.session.add_all(comments)

    # Commit all changes to the database
    db.session.commit()
    print("Database seeded successfully!")
